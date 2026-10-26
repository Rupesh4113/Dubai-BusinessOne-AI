import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    layer1_cache_stats: {
      total_cached_entries: 12,
      total_hits: 18,
      total_misses: 6,
      hit_ratio_percent: 75.0,
      estimated_zero_inference_tokens_saved: 14400,
    },
    layer4_pending_approvals_count: 1,
  });
}
