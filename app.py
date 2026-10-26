"""Entrypoint alias for Streamlit Cloud."""
import os
import sys

# Run streamlit_app.py
if __name__ == "__main__":
    import streamlit.web.bootstrap as bootstrap
    app_path = os.path.join(os.path.dirname(__file__), "streamlit_app.py")
    bootstrap.run(app_path, False, [], flag_options={})
else:
    # If imported directly as a module by Streamlit runner
    with open(os.path.join(os.path.dirname(__file__), "streamlit_app.py"), encoding="utf-8") as f:
        code = compile(f.read(), "streamlit_app.py", "exec")
        exec(code, globals())
