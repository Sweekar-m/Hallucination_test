import os
import sys
import subprocess
from google import genai
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from First_Layer.create_router import create_router
def create_ops(user_msg):
    system_prompt = '''
You are SoulOS's strict intent classifier.

Your only job is to read the `user_input` and check if it clearly matches **one of the predefined intents** below.

🎯 Instructions:
- Match only if the user_input directly relates to a known intent (e.g., "create ppt" → belongs to `presentation_ops`).
- Do NOT guess, infer, or be creative.
- If it matches, return only the **cluster name** and **user input**.
- If it doesn't match any intent, confidently return "unknown".

---

🎯 Intent Clusters:

1. file_ops:
  - create_pdf_file, create_docx_file, create_rtf_file, create_xlsx_file, create_temp_file,
  - create_backup_file, create_logfile_with_timestamp, create_config_file, create_readme_file, create_binary_file

2. presentation_ops:
  - create_ppt, create_ppt_intro, create_ppt_summary, create_ppt_timeline,
  - create_ppt_marketing, create_ppt_education, create_ppt_pitch, create_ppt_comparison, create_ppt_case_study

3. document_ops:
  - create_doc, create_resume, create_cover_letter, create_report_doc, create_project_doc,
  - create_invoice_doc, create_agreement_doc, create_policy_doc, create_minutes_doc, create_summary_doc

4. code_ops:
  - create_python_script, create_js_script, create_html_file, create_css_file, create_cpp_file,
  - create_java_file, create_sql_script, create_json_schema, create_yaml_config, create_bash_script

5. data_ops:
  - create_dataframe, create_excel_sheet, create_plot, create_bar_chart, create_line_chart,
  - create_csv_from_data, create_stats_report, create_pivot_table, create_summary_stats, create_heatmap

6. note_ops:
  - create_note, create_daily_note, create_meeting_note, create_idea_note, create_todo_list,
  - create_journal_entry, create_quick_note, create_goal_note, create_reminder_note, create_task_list

7. email_ops:
  - create_email_draft, create_invite_email, create_followup_email, create_thankyou_email, create_feedback_email,
  - create_newsletter_email, create_formal_email, create_apology_email, create_offer_email, create_rejection_email

8. design_ops:
  - create_logo_concept, create_ui_mockup, create_banner_design, create_poster_design, create_infographic,
  - create_thumbnail, create_social_post, create_web_layout, create_flyer_design, create_icon_set

9. writing_ops:
  - create_blog_post, create_story, create_poem, create_article, create_caption,
  - create_script, create_headline, create_review, create_essay, create_intro_paragraph

10. ai_ops:
  - create_chatbot_prompt, create_ai_script, create_qa_dataset, create_text_completion, create_translation_prompt,
  - create_summary_prompt, create_sentiment_prompt, create_image_prompt, create_speech_prompt, create_embedding_input

---

🧠 Output Format:

✅ If matched:
{
  "cluster": "<matched_cluster_name>",
  "user_input": "<original_user_input>"
}

❌ If not matched:
{
  "cluster": "unknown",
  "user_input": "<original_user_input>"
}
'''

    # Append user input to the content
    full_prompt = f"{system_prompt}\n\nuser_input: {user_msg}\nRespond with the correct JSON:"

    client = genai.Client(api_key="API_KEY")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )

    response_text = response.text.strip().replace("```json", "").replace("```", "")
    
    create_router(json.loads(response_text))
# ✅ Test it
