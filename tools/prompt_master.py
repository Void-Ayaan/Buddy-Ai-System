import re
import threading
import warnings

warnings.filterwarnings('ignore')

def search_topic_keywords(idea):
    """Perform quick 1-second domain research extraction on the user's idea."""
    summary_container = [""]
    
    def _search():
        try:
            import importlib
            DDGS = None
            for mod_name in ["duckduckgo_search", "ddgs"]:
                try:
                    mod = importlib.import_module(mod_name)
                    DDGS = getattr(mod, "DDGS", None)
                    if DDGS:
                        break
                except Exception:
                    pass

            if DDGS:
                with DDGS() as ddgs:
                    results = list(ddgs.text(idea, max_results=2))
                    if results:
                        snippets = [r.get('body', '') for r in results if r.get('body')]
                        summary_container[0] = " ".join(snippets[:2])
        except Exception:
            pass

    t = threading.Thread(target=_search, daemon=True)
    t.start()
    t.join(timeout=1.2) # Fast 1.2s non-blocking timeout
    return summary_container[0]

def create_master_prompt(user_idea):
    """
    Buddy Prompt Architect Protocol:
    1. Listens to user's raw idea ("buddy listen and make prompt [idea]").
    2. Researches domain context.
    3. Crafts a bulletproof, universal Master Prompt ready to copy-paste into any AI model.
    """
    raw_idea = user_idea.strip()
    if not raw_idea:
        return "Please provide an idea for the prompt (e.g., 'buddy listen and make prompt for a python web scraper')."

    # Clean trigger prefix from input if present
    clean_idea = re.sub(r"^(?:buddy\s+listen\s+and\s+make\s+prompt|buddy\s+make\s+prompt|make\s+prompt|create\s+prompt|master\s+prompt|build\s+prompt|write\s+prompt)\s+(?:for\s+)?", "", raw_idea, flags=re.IGNORECASE).strip()
    if not clean_idea:
        clean_idea = raw_idea

    # Conduct background research enrichment
    research_summary = search_topic_keywords(clean_idea)
    research_context = f"\n[Domain Knowledge Context: {research_summary[:300]}...]" if research_summary else ""

    # Infer domain persona and guidelines
    clean_lower = clean_idea.lower()
    if any(k in clean_lower for k in ["code", "python", "app", "website", "html", "javascript", "react", "next.js", "api", "backend", "database", "bot", "store", "ecommerce", "script"]):
        role = "Senior Full-Stack Software Architect and Principal Engineer"
        tone = "Technical, highly precise, production-ready, clean code-focused"
        deliverables = "Complete, production-grade code snippets, directory architecture breakdown, error handling, and deployment steps."
    elif any(k in clean_lower for k in ["essay", "story", "write", "book", "article", "blog", "content", "script", "copy"]):
        role = "World-Class Author, Creative Director, and Content Strategist"
        tone = "Engaging, compelling, beautifully structured, highly articulate"
        deliverables = "Deeply researched, captivating content with clear section headers, engaging narrative arc, and zero filler."
    elif any(k in clean_lower for k in ["design", "image", "logo", "ui", "ux", "art", "midjourney", "photoshop"]):
        role = "Lead UI/UX Designer and AI Art Director"
        tone = "Visual, precise, aesthetic-focused, parameter-rich"
        deliverables = "Detailed visual design specs, layout grids, color tokens, typography hierarchy, or exact Midjourney parameters."
    else:
        role = "Principal Subject Matter Expert and Strategic Consultant"
        tone = "Professional, analytical, authoritative, actionable"
        deliverables = "In-depth analysis, structured framework, step-by-step strategy, and concrete actionable guidelines."

    master_prompt_text = f"""# ROLE & SYSTEM PERSONA
You are an elite {role}. Your objective is to execute the following user request with absolute precision, technical depth, and state-of-the-art standards.

# CONTEXT & GOAL
Objective: "{clean_idea}"{research_context}

# CORE DELIVERABLES & METHODOLOGY
1. **Requirements Analysis**: Break down the core components, implicit edge cases, and industry best practices.
2. **Implementation Strategy**: Provide {deliverables}
3. **Execution Quality Standards**:
   - Ensure all output is rigorous, robust, and directly usable.
   - Do NOT use generic placeholders or vague summaries. Write out complete, concrete solutions.
   - Maintain a {tone} tone throughout.

# OUTPUT STRUCTURE
- **Section 1: Executive Overview**: High-level summary of the solution architecture.
- **Section 2: Complete Implementation / Output**: Full step-by-step code or content deliverables.
- **Section 3: Optimization & Next Steps**: Best practices, security tips, and edge-case handling.

# CONSTRAINTS
- Zero fluff or redundant meta-commentary.
- Focus strictly on maximum technical value, clarity, and precision.
- Begin your response immediately with Section 1.
"""

    response = f"Boss, I listened carefully to your idea, researched domain context, and created a Master Prompt! You can copy and paste this into any AI (ChatGPT, Claude, Gemini, DeepSeek):\n\n```markdown\n{master_prompt_text}\n```"
    return response
