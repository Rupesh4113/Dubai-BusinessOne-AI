"""Master Agent Orchestrator and Operational State Machine for Dubai BusinessOne AI."""

import time
import uuid
from typing import Dict, Any, Optional
from decimal import Decimal
from .state import AgentTaskState
from .intent_classifier import sanitize_and_check_safety, classify_intent_and_extract_entities
from .risk_assessor import evaluate_action_risk
from .approval_gate import approval_gate
from .model_router import model_router
from ..memory import memory_manager, layer4_history
from ..tools import tool_registry
from ..calculator import (
    calculate_dubai_det_fees,
    calculate_dubai_chamber_fee,
    calculate_uae_corporate_tax,
    calculate_uae_vat,
    convert_currency,
    DubaiDETFeeRequest,
    DubaiChamberFeeRequest,
    CorporateTaxRequest,
    VATCalculationRequest,
    CurrencyConversionRequest
)
from ..knowledge import generate_citations, RegulatoryRecord


class AgentOrchestrator:
    """End-to-End Orchestrator executing the secure operations state machine."""

    def process_request(
        self,
        prompt: str,
        tenant_id: str = "demo_tenant_dubai",
        user_id: str = "user_admin_001",
        language: str = "en",
        idempotency_key: Optional[str] = None,
        approval_token: Optional[str] = None
    ) -> AgentTaskState:
        """Executes the full agent workflow lifecycle."""
        task_id = f"TASK-{int(time.time())}-{uuid.uuid4().hex[:6]}"
        state = AgentTaskState(
            task_id=task_id,
            tenant_id=tenant_id,
            user_id=user_id,
            raw_prompt=prompt,
            language=language
        )

        # -------------------------------------------------------------
        # STEP 1: Input Sanitization & Prompt-Injection Defense
        # -------------------------------------------------------------
        sanitized_text, is_safe, safety_msg = sanitize_and_check_safety(prompt)
        state.sanitized_prompt = sanitized_text
        state.audit_trail.append(f"Step 1 [Sanitization]: Safety Check {'PASSED' if is_safe else 'FAILED'}")

        if not is_safe:
            state.current_step = "FAILED"
            state.error_message = safety_msg
            state.final_response_text = f"Security Policy Violation: {safety_msg}"
            layer4_history.create_task(tenant_id, user_id, "prompt_injection_intercepted", "CRITICAL", {"prompt": prompt})
            return state

        # -------------------------------------------------------------
        # STEP 2: Layer 1 Zero-Inference Exact Answer Cache Check
        # -------------------------------------------------------------
        cached_entry = memory_manager.check_layer1_exact_match(
            tenant_id=tenant_id,
            query=sanitized_text,
            language=language
        )
        if cached_entry:
            state.current_step = "COMPLETED"
            state.is_cached_zero_inference = True
            state.final_response_text = cached_entry.response_data.get("final_response_text", "")
            state.structured_output = cached_entry.response_data.get("structured_output", {})
            state.retrieved_knowledge = cached_entry.response_data.get("retrieved_knowledge", [])
            state.citations = cached_entry.response_data.get("citations", [])
            state.intermediate_calculations = cached_entry.response_data.get("intermediate_calculations", {})
            state.audit_trail.append(f"Step 2 [Zero-Inference Cache]: Cache HIT (Key: {cached_entry.cache_key[:12]}...). Served without LLM inference.")
            return state

        state.audit_trail.append("Step 2 [Zero-Inference Cache]: Cache MISS. Proceeding to task planning.")

        # -------------------------------------------------------------
        # STEP 3: Intent Classification & Entity Extraction
        # -------------------------------------------------------------
        intent, entities = classify_intent_and_extract_entities(sanitized_text)
        state.intent = intent
        state.extracted_entities = entities
        state.audit_trail.append(f"Step 3 [Intent Classification]: Identified Intent '{intent}' with {len(entities)} extracted parameters.")

        # -------------------------------------------------------------
        # STEP 4: Layer 2 Verified Knowledge Retrieval & Citations
        # -------------------------------------------------------------
        retrieved_raw = memory_manager.query_layer2_knowledge(sanitized_text, max_results=3)
        state.retrieved_knowledge = retrieved_raw

        # Format citations
        formatted_cits = []
        for r in retrieved_raw:
            formatted_cits.append({
                "authority_name": r.get("issuing_authority"),
                "statutory_law": r.get("statutory_law"),
                "official_source_url": r.get("official_source_url"),
                "freshness_status": r.get("freshness", {}).get("status", "FRESH")
            })
        state.citations = formatted_cits
        state.audit_trail.append(f"Step 4 [Knowledge Retrieval]: Retrieved {len(retrieved_raw)} verified official regulatory clauses.")

        # -------------------------------------------------------------
        # STEP 5: Deterministic Numerical & Fee Calculations
        # -------------------------------------------------------------
        calcs: Dict[str, Any] = {}

        if intent in ["BUSINESS_SETUP_INQUIRY", "TRADE_NAME_RESERVATION"]:
            # 1. DET Setup calculation
            rent_val = Decimal(str(entities.get("annual_office_rent", 60000)))
            det_res = calculate_dubai_det_fees(DubaiDETFeeRequest(
                license_type="commercial",
                annual_office_rent_aed=rent_val
            ))
            calcs["det_setup"] = det_res.model_dump()

            # 2. Dubai Chamber membership fee
            chamber_res = calculate_dubai_chamber_fee(DubaiChamberFeeRequest(
                legal_form="llc",
                share_capital=Decimal("300000.00")
            ))
            calcs["chamber_membership"] = chamber_res.model_dump()

            # 3. Corporate Tax estimate if revenue provided
            proj_rev = entities.get("projected_revenue", 1200000.0)
            est_profit = Decimal(str(proj_rev * 0.25))  # 25% profit margin baseline
            ct_res = calculate_uae_corporate_tax(CorporateTaxRequest(
                taxable_net_profit=est_profit,
                annual_revenue=Decimal(str(proj_rev))
            ))
            calcs["corporate_tax"] = ct_res.model_dump()

            # 4. Standard VAT on services
            vat_res = calculate_uae_vat(VATCalculationRequest(
                amount=Decimal(str(proj_rev)),
                vat_category="standard"
            ))
            calcs["vat"] = vat_res.model_dump()

        elif intent == "CORPORATE_TAX_CALCULATION":
            profit_val = Decimal(str(entities.get("taxable_net_profit", 500000)))
            ct_res = calculate_uae_corporate_tax(CorporateTaxRequest(
                taxable_net_profit=profit_val
            ))
            calcs["corporate_tax"] = ct_res.model_dump()

        elif intent == "VAT_CALCULATION":
            amt_val = Decimal(str(entities.get("amount", 10000)))
            vat_res = calculate_uae_vat(VATCalculationRequest(
                amount=amt_val,
                vat_category="standard"
            ))
            calcs["vat"] = vat_res.model_dump()

        elif intent == "CURRENCY_CONVERSION":
            amt_val = Decimal(str(entities.get("amount", 1000)))
            fx_res = convert_currency(CurrencyConversionRequest(
                amount=amt_val,
                from_currency="USD",
                to_currency="AED"
            ))
            calcs["currency_conversion"] = fx_res.model_dump()

        state.intermediate_calculations = calcs
        state.audit_trail.append(f"Step 5 [Deterministic Calculation]: Completed {len(calcs)} statutory mathematical calculations using Decimal precision.")

        # -------------------------------------------------------------
        # STEP 6: Risk Assessment & Policy Gate
        # -------------------------------------------------------------
        planned_tool_names = []
        if intent == "TRADE_NAME_RESERVATION":
            planned_tool_names.append("official_registry_search")
            planned_tool_names.append("trade_license_reservation")
        elif intent == "INVOICE_RECONCILIATION":
            planned_tool_names.append("invoice_reconciler")
        elif intent == "BUSINESS_SETUP_INQUIRY":
            planned_tool_names.append("official_registry_search")
            planned_tool_names.append("document_generator")

        risk_level, req_approval, risk_rationale = evaluate_action_risk(intent, entities, planned_tool_names)
        state.risk_level = risk_level
        state.requires_human_approval = req_approval
        state.audit_trail.append(f"Step 6 [Risk Assessment]: Assigned Risk Tier '{risk_level}'. Requires Human Approval: {req_approval}")

        # Record task in Layer 4 history
        task_record = layer4_history.create_task(
            tenant_id=tenant_id,
            user_id=user_id,
            action_name=intent,
            risk_level=risk_level,
            input_parameters={"prompt": prompt, "entities": entities},
            idempotency_key=idempotency_key
        )

        # -------------------------------------------------------------
        # STEP 7: Human Approval Gate for High-Risk Actions
        # -------------------------------------------------------------
        if req_approval:
            # Check if valid approval token was provided in this call
            if approval_token:
                valid_approval, msg = approval_gate.verify_and_grant_approval(task_record.task_id, approval_token, user_id)
                if valid_approval:
                    state.is_approved_by_human = True
                    state.approved_by = user_id
                    state.audit_trail.append(f"Step 7 [Approval Gate]: Token verified. Human supervisor '{user_id}' authorized action.")
                else:
                    state.current_step = "PENDING_APPROVAL"
                    state.error_message = f"Invalid approval token: {msg}"
                    state.audit_trail.append(f"Step 7 [Approval Gate]: {msg}")
                    state.final_response_text = model_router.route_and_synthesize(
                        intent, sanitized_text, language, retrieved_raw, calcs, [], risk_level,
                        pending_approval=True, approval_token=task_record.approval_token
                    )
                    return state
            else:
                # Generate new one-time token and hold
                generated_token = approval_gate.generate_approval_request(task_record.task_id, f"Reservation for {entities.get('company_name')}", entities)
                state.current_step = "PENDING_APPROVAL"
                state.approval_token = generated_token
                state.audit_trail.append(f"Step 7 [Approval Gate]: Action paused. Human Approval Token generated: {generated_token}")

                state.final_response_text = model_router.route_and_synthesize(
                    intent, sanitized_text, language, retrieved_raw, calcs, [], risk_level,
                    pending_approval=True, approval_token=generated_token
                )
                return state

        # -------------------------------------------------------------
        # STEP 8: Tool Execution Sandbox & Postcondition Verification
        # -------------------------------------------------------------
        executed_tool_results = []
        exec_context = {
            "human_approved": state.is_approved_by_human or not req_approval,
            "approval_token": approval_token or state.approval_token,
            "approved_by": state.approved_by or user_id,
            "tenant_id": tenant_id
        }

        # 1. Search name availability if needed
        if "official_registry_search" in planned_tool_names:
            comp_name = entities.get("company_name", "Apex Global Solutions")
            res_tool = tool_registry.execute_tool("official_registry_search", {"query": comp_name, "search_type": "name_availability"}, exec_context)
            executed_tool_results.append(res_tool.model_dump())
            state.audit_trail.extend(res_tool.audit_trail)

        # 2. Execute reservation if approved
        if "trade_license_reservation" in planned_tool_names and state.is_approved_by_human:
            res_tool = tool_registry.execute_tool("trade_license_reservation", {
                "company_name": entities.get("company_name", "Apex Global Solutions LLC"),
                "share_capital": 300000
            }, exec_context)
            executed_tool_results.append(res_tool.model_dump())
            state.audit_trail.extend(res_tool.audit_trail)

        # 3. Generate summary document if business setup inquiry
        if "document_generator" in planned_tool_names:
            doc_tool = tool_registry.execute_tool("document_generator", {
                "title": f"Dubai Mainland Setup Dossier — {entities.get('company_name', 'Commercial LLC')}",
                "sections": {
                    "summary": f"Initial operational analysis for commercial entity formation in Dubai Mainland with projected year-1 revenue of AED {entities.get('projected_revenue', '1,200,000')}."
                },
                "citations": formatted_cits
            }, exec_context)
            executed_tool_results.append(doc_tool.model_dump())
            state.audit_trail.extend(doc_tool.audit_trail)

        state.executed_tools = executed_tool_results

        # -------------------------------------------------------------
        # STEP 9: Response Synthesis & Verification
        # -------------------------------------------------------------
        state.final_response_text = model_router.route_and_synthesize(
            intent=intent,
            prompt=sanitized_text,
            language=language,
            retrieved_knowledge=retrieved_raw,
            calculations=calcs,
            executed_tools=executed_tool_results,
            risk_level=risk_level,
            pending_approval=False
        )
        state.current_step = "COMPLETED"

        # Update Layer 4 execution record
        layer4_history.mark_executed(task_record.task_id, {
            "calculations": calcs,
            "executed_tools": executed_tool_results,
            "response": state.final_response_text
        })

        # -------------------------------------------------------------
        # STEP 10: Store Verified Safe Responses in Layer 1 Cache
        # -------------------------------------------------------------
        if risk_level == "LOW" and not req_approval:
            memory_manager.record_layer1_verified_answer(
                tenant_id=tenant_id,
                query=sanitized_text,
                response_data={
                    "final_response_text": state.final_response_text,
                    "structured_output": state.structured_output,
                    "retrieved_knowledge": state.retrieved_knowledge,
                    "citations": state.citations,
                    "intermediate_calculations": state.intermediate_calculations
                },
                language=language
            )
            state.audit_trail.append("Step 10 [Zero-Inference Cache]: Persisted verified response to Layer 1 Cache for future zero-cost instant retrieval.")

        return state


orchestrator = AgentOrchestrator()
