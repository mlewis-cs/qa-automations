---
name: HELPER-db-investigator
description: "Use this agent when we need DB information to investigate a problem"
tools: mcp__ide__getDiagnostics, mcp__ide__executeCode
model: haiku
color: cyan
---

You use SQL to investigate and return useful query results related to your given prompt

DB SCHEMA:

Table: activities
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - recorded_at: TIMESTAMP WITHOUT TIME ZONE
  - firm_id: INTEGER -> firms._id
  - case_id: INTEGER -> cases._id
  - sub_user_id: INTEGER
  - sub_user_type: TEXT
  - user_name: TEXT
  - activity_name: TEXT
  - payload: JSONB
  - type: VARCHAR
  - platform: VARCHAR

Table: ai_case_summaries
  - id: INTEGER [PK] NOT NULL
  - firm_id: INTEGER -> firms._id
  - case_id: INTEGER -> cases._id
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - summary: JSONB
  - input_payload: JSONB
  - ai_transaction_id: INTEGER

Table: ai_transactions
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - start: TIMESTAMP WITHOUT TIME ZONE
  - end: TIMESTAMP WITHOUT TIME ZONE
  - exception: TEXT
  - response_json: TEXT
  - request_json: TEXT
  - firm_id: INTEGER

Table: api_keys
  - id: INTEGER [PK] NOT NULL
  - firm_id: INTEGER -> firms._id
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - api_key: TEXT
  - is_active: BOOLEAN
  - sub_user_id: INTEGER -> sub_users.id
  - type: TEXT
  - deactivate_throttle: BOOLEAN

Table: api_transactions
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - start: TIMESTAMP WITHOUT TIME ZONE
  - end: TIMESTAMP WITHOUT TIME ZONE
  - exception: TEXT
  - payload: TEXT
  - function_name: TEXT
  - firm_id: INTEGER

Table: appointment_attendees
  - appointment_id: INTEGER -> appointments._id
  - attendee_id: INTEGER -> users._id

Table: appointments
  - id: INTEGER [PK] NOT NULL
  - case_id: INTEGER -> cases._id
  - office_name: TEXT
  - address: TEXT
  - provider_name: TEXT
  - description: TEXT
  - treatment_notes: TEXT
  - treatment_type_id: INTEGER -> treatment_types._id
  - feeling_rating: INTEGER
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - appointment_date: TIMESTAMP WITHOUT TIME ZONE
  - treatment_date: TIMESTAMP WITHOUT TIME ZONE
  - type: TEXT
  - appointment_title: TEXT
  - appointment_attendees: TEXT
  - integration_id: TEXT
  - appointment_end_date: TIMESTAMP WITHOUT TIME ZONE
  - confirmation_enabled: BOOLEAN
  - confirmation_send_date: TIMESTAMP WITHOUT TIME ZONE
  - confirmation_sent_date: TIMESTAMP WITHOUT TIME ZONE
  - internal_notification_enabled: BOOLEAN
  - internal_notification_send_date: TIMESTAMP WITHOUT TIME ZONE
  - internal_notification_sent_date: TIMESTAMP WITHOUT TIME ZONE
  - client_confirmed_appointment: BOOLEAN

Table: attorneys
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - user_id: INTEGER -> users._id
  - firm_id: INTEGER -> firms._id
  - bio: TEXT
  - contact_email_address: TEXT
  - business_number: TEXT
  - wants_sms: BOOLEAN
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - integration_id: TEXT
  - descriptor: TEXT
  - case_notifications_off: BOOLEAN
  - last_digest: TIMESTAMP WITHOUT TIME ZONE
  - wants_daily_digest: BOOLEAN
  - wants_ics_invites: BOOLEAN
  - calendar_type: calendar_types
  - send_as_primary: BOOLEAN
  - wants_exception_reporting: BOOLEAN
  - wants_email_notifications: BOOLEAN
  - wants_email_notification_types: TEXT[]
  - receive_unknown_client_notification: BOOLEAN
  - preferences: JSONB
  - onboarding_seen: TEXT[]

Table: audit_trails
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - record_table: TEXT
  - record_id: INTEGER
  - action: TEXT
  - payload: TEXT
  - update_summary: TEXT
  - original_value: TEXT
  - updated_value: TEXT
  - user_permissions: TEXT
  - user_type: TEXT
  - request_metadata: TEXT
  - user_id: INTEGER -> users._id
  - firm_id: INTEGER -> firms._id

Table: automation_heartbeats
  - id: INTEGER [PK] NOT NULL
  - name: TEXT
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - deactivated: BOOLEAN
  - success: BOOLEAN
  - created_by_user_id: INTEGER -> users._id
  - automation_id: INTEGER -> automations._id

Table: automation_templates
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - firm_id: INTEGER NOT NULL -> firms._id
  - content: TEXT NOT NULL
  - statuses: INTEGER[] NOT NULL
  - created_by_user_id: INTEGER NOT NULL -> users._id
  - case_type_id: INTEGER NOT NULL -> case_types._id
  - checklist_template_id: INTEGER -> checklist_templates._id
  - message_template_id: INTEGER -> message_templates._id
  - retroactive: BOOLEAN NOT NULL
  - automation_type: TEXT
  - days_of_week: INTEGER[]
  - days_of_month: INTEGER[]
  - months_of_year: INTEGER[]
  - hour_of_day: INTEGER
  - days_after_event: INTEGER
  - call_limit: INTEGER
  - hold_until_activation: BOOLEAN
  - date_type: automation_date_types
  - run_closed: BOOLEAN
  - run_hold: BOOLEAN
  - nps_scores: INTEGER[]
  - frequency_amount: INTEGER
  - frequency_type: frequency_type_enum

Table: automations
  - id: INTEGER [PK] NOT NULL
  - case_id: INTEGER -> cases._id
  - firm_id: INTEGER -> firms._id
  - automation_template_id: INTEGER -> automation_templates._id
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - last_run_date: TIMESTAMP WITHOUT TIME ZONE
  - automation_type: TEXT
  - days_of_week: INTEGER[]
  - days_of_month: INTEGER[]
  - months_of_year: INTEGER[]
  - hour_of_day: INTEGER
  - days_after_event: INTEGER
  - content: TEXT
  - error_message: TEXT
  - call_limit: INTEGER
  - call_count: INTEGER
  - hold_until_activation: BOOLEAN
  - date_type: automation_date_types
  - client_id: INTEGER -> clients.id
  - run_closed: BOOLEAN
  - run_hold: BOOLEAN
  - info_message: TEXT
  - nps_scores: INTEGER[]
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - last_send_date: TIMESTAMP WITHOUT TIME ZONE
  - send_date: TIMESTAMP WITHOUT TIME ZONE
  - send_date_last_calculated: TIMESTAMP WITHOUT TIME ZONE
  - send_date_calculation_error: TIMESTAMP WITHOUT TIME ZONE
  - send_date_calculation_log: TEXT
  - runtime_exception: TEXT
  - file_id: INTEGER -> files._id
  - frequency_amount: INTEGER
  - frequency_type: frequency_type_enum

Table: bulk_actions
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - scheduled_send_date: TIMESTAMP WITHOUT TIME ZONE
  - started_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - disabled_at: TIMESTAMP WITHOUT TIME ZONE
  - message_content: TEXT
  - error_message: TEXT
  - case_count: INTEGER
  - cases_processed: INTEGER
  - cases_successful: INTEGER
  - completed_at: TIMESTAMP WITHOUT TIME ZONE
  - method_type: TEXT
  - retry_attempts: INTEGER
  - firm_id: INTEGER -> firms._id
  - request_user_id: INTEGER -> users._id
  - results_csv_file_url: TEXT -> files._id
  - validated_at: TIMESTAMP WITHOUT TIME ZONE
  - initiated_by: TEXT
  - last_processed_timestamp: TIMESTAMP WITHOUT TIME ZONE

Table: calendar_events
  - id: INTEGER [PK] NOT NULL
  - created_by_id: INTEGER -> users._id
  - updated_by_id: INTEGER -> users._id
  - appointment_id: INTEGER -> appointments._id
  - created_for_attorney: INTEGER -> attorneys.id
  - created_for_paralegal: INTEGER -> paralegals.id
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - calendar_id: TEXT
  - event_id: TEXT
  - calendar_type: calendar_types
  - sequence_num: INTEGER

Table: case_bulk_messages
  - id: INTEGER [PK] NOT NULL
  - case_id: INTEGER -> cases._id
  - file_id: INTEGER -> files._id
  - message_id: INTEGER -> messages._id
  - bulk_action_id: INTEGER -> bulk_actions._id
  - content: TEXT
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - processed_at: TIMESTAMP WITHOUT TIME ZONE
  - exception: TEXT
  - scheduled_message_send_date: TIMESTAMP WITHOUT TIME ZONE
  - sender_id: INTEGER -> users._id
  - invite_clients: BOOLEAN
  - message_template_type: TEXT
  - translation_edited: BOOLEAN
  - retry_attempts: INTEGER

Table: case_status_durations
  - id: INTEGER [PK] NOT NULL
  - firm_id: INTEGER -> firms._id
  - case_id: INTEGER -> cases._id
  - case_type_id: INTEGER -> case_types._id
  - previous_case_status_id: INTEGER -> case_statuses._id
  - current_case_status_id: INTEGER -> case_statuses._id
  - case_closed: BOOLEAN
  - case_on_hold: BOOLEAN
  - order: INTEGER
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE

Table: case_status_templates
  - id: INTEGER [PK] NOT NULL
  - case_type_template_id: INTEGER -> case_type_templates._id
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - description: TEXT
  - name: TEXT
  - number: INTEGER
  - updated_at: TIMESTAMP WITHOUT TIME ZONE

Table: case_status_transitions
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - source_case_status_id: INTEGER -> case_statuses._id
  - target_case_status_id: INTEGER -> case_statuses._id
  - target_case_type_id: INTEGER -> case_types._id
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE

Table: case_statuses
  - id: INTEGER [PK] NOT NULL
  - case_type_id: INTEGER -> case_types._id
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - description: TEXT
  - firm_id: INTEGER -> firms._id
  - name: TEXT
  - import_names: TEXT[]
  - display_nps: BOOLEAN
  - number: INTEGER
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - video_id: INTEGER -> videos._id
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - draft: BOOLEAN
  - import_names_confirmed_at: TIMESTAMP WITHOUT TIME ZONE
  - description_confirmed_at: TIMESTAMP WITHOUT TIME ZONE
  - ai_generated_at: TIMESTAMP WITHOUT TIME ZONE

Table: case_type_templates
  - id: INTEGER [PK] NOT NULL
  - practice_area_template_id: INTEGER -> practice_area_templates._id
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - name: TEXT
  - updated_at: TIMESTAMP WITHOUT TIME ZONE

Table: case_types
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - firm_id: INTEGER -> firms._id
  - name: TEXT
  - import_names: TEXT[]
  - imported: BOOLEAN
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - settings: JSONB
  - closed_integration_stages: TEXT[]
  - draft: BOOLEAN
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - import_names_confirmed_at: TIMESTAMP WITHOUT TIME ZONE
  - settings_confirmed_at: TIMESTAMP WITHOUT TIME ZONE
  - pdi_created_at: TIMESTAMP WITHOUT TIME ZONE
  - ai_generated_at: TIMESTAMP WITHOUT TIME ZONE

Table: cases
  - id: INTEGER [PK] NOT NULL
  - primary_attorney_id: INTEGER -> attorneys.id
  - primary_attorney_sub_user_id: INTEGER -> sub_users.id
  - case_status_id: INTEGER -> case_statuses._id
  - case_type_id: INTEGER -> case_types._id
  - group: TEXT
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - closed_date: TIMESTAMP WITHOUT TIME ZONE
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - description: TEXT
  - firm_id: INTEGER -> firms._id
  - closed_by_child_id: INTEGER -> sub_users.child_id
  - closed_by_id: INTEGER -> users._id
  - date: DATE
  - on_hold: BOOLEAN
  - on_hold_explanation: TEXT
  - notes: TEXT
  - readable_id: TEXT
  - integration_id: TEXT
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - wants_sms: BOOLEAN
  - activated_date: TIMESTAMP WITHOUT TIME ZONE
  - referred_at: TIMESTAMP WITHOUT TIME ZONE
  - referral_source: TEXT
  - review_sent_at: TIMESTAMP WITHOUT TIME ZONE
  - wants_sms_set: TIMESTAMP WITHOUT TIME ZONE
  - is_imported: BOOLEAN
  - integration_used: TEXT
  - most_recent_message_sent_at: TIMESTAMP WITHOUT TIME ZONE
  - most_recent_message_content: TEXT
  - most_recent_message_id: INTEGER
  - is_communication: BOOLEAN
  - case_status_updated_manually: BOOLEAN
  - case_status_updated_by_id: INTEGER
  - most_recent_nps: INTEGER
  - target_language: TEXT
  - fv_case_note_id: INTEGER
  - fv_case_appointment_id: INTEGER
  - fv_case_internal_message_id: INTEGER
  - translation_enabled: BOOLEAN
  - translation_updated_at: TIMESTAMP WITHOUT TIME ZONE
  - mycase_message_thread_id: INTEGER
  - mycase_message_thread_request_at: TIMESTAMP WITHOUT TIME ZONE
  - inbound_translate_count: INTEGER
  - outbound_translate_count: INTEGER
  - recommended_response_feature_enabled_at: TIMESTAMP WITHOUT TIME ZONE
  - activation_failed_reason: TEXT
  - ai_summary_feature_enabled_at: TIMESTAMP WITHOUT TIME ZONE
  - custom_branding_id: INTEGER -> custom_brandings._id
  - most_recent_csat_survey_id: INTEGER
  - predicted_detractor: BOOLEAN

Table: cases_attorneys
  - case_id: INTEGER -> cases._id
  - attorney_id: INTEGER -> attorneys.id
  - notifications_off: BOOLEAN
  - notification_settings_updated_by: INTEGER -> users._id
  - notification_settings_updated_at: TIMESTAMP WITHOUT TIME ZONE

Table: cases_clients
  - case_id: INTEGER -> cases._id
  - client_id: INTEGER -> clients.id

Table: cases_files
  - case_id: INTEGER -> cases._id
  - file_id: INTEGER -> files._id

Table: cases_organizations
  - case_id: INTEGER -> cases._id
  - organization_id: INTEGER -> organizations._id
  - can_chat: BOOLEAN
  - show_case_status: BOOLEAN
  - show_client_names: BOOLEAN

Table: cases_paralegals
  - case_id: INTEGER -> cases._id
  - paralegal_id: INTEGER -> paralegals.id
  - notifications_off: BOOLEAN
  - notification_settings_updated_by: INTEGER -> users._id
  - notification_settings_updated_at: TIMESTAMP WITHOUT TIME ZONE

Table: celery_tasks
  - id: INTEGER [PK] NOT NULL
  - task_id: TEXT
  - task_name: TEXT
  - state: TEXT
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - kwargs: TEXT
  - firm_id: INTEGER -> firms._id
  - requesting_user_id: INTEGER -> users._id
  - error_message: TEXT

Table: chat_files
  - id: INTEGER [PK] NOT NULL
  - chat_id: INTEGER NOT NULL -> chats._id
  - sender_child_id: INTEGER
  - sender_type: INTEGER
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - file_name: TEXT
  - content_type: TEXT
  - extension: TEXT
  - size: INTEGER
  - chat_message_id: INTEGER -> chat_messages._id
  - s3_key: TEXT
  - thumbnail_s3_key: TEXT
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - uploaded_to_s3: BOOLEAN

Table: chat_messages
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - synced_at: TIMESTAMP WITHOUT TIME ZONE
  - integration_error: TEXT
  - internal_integration_error: TEXT
  - sender_id: INTEGER -> users._id
  - sender_type: TEXT
  - sender_child_id: INTEGER
  - sender_name: TEXT
  - content: TEXT NOT NULL
  - chat_id: INTEGER NOT NULL -> chats._id
  - case_id: INTEGER -> cases._id
  - status_number: INTEGER
  - type: TEXT
  - checklist_item_id: INTEGER -> checklist_items._id
  - treatment_id: INTEGER -> appointments._id
  - nps_id: INTEGER -> net_promoter_scores._id
  - is_automated_defunct: BOOLEAN
  - automated_message_type: TEXT
  - firm_id: INTEGER -> firms._id
  - sent_at: TIMESTAMP WITHOUT TIME ZONE

Table: chat_notifications
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - recipient_child_id: INTEGER NOT NULL
  - recipient_type: TEXT NOT NULL
  - read_at: TIMESTAMP WITHOUT TIME ZONE
  - sender_name: TEXT
  - content: TEXT
  - chat_message_id: INTEGER NOT NULL -> chat_messages._id
  - chat_id: INTEGER NOT NULL -> chats._id
  - case_id: INTEGER -> cases._id
  - type: TEXT
  - email_sent_at: TIMESTAMP WITHOUT TIME ZONE
  - email_delivered_at: TIMESTAMP WITHOUT TIME ZONE
  - email_interacted_type: TEXT
  - email_interacted_at: TIMESTAMP WITHOUT TIME ZONE
  - email_unique_token: TEXT

Table: chats
  - id: INTEGER [PK] NOT NULL
  - chat_name: TEXT
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - case_id: INTEGER -> cases._id
  - organization_id: INTEGER -> organizations._id
  - firm_id: INTEGER -> firms._id

Table: chats_attorneys
  - chat_id: INTEGER -> chats._id
  - attorney_id: INTEGER -> attorneys.id

Table: chats_members
  - chat_id: INTEGER -> chats._id
  - member_id: INTEGER -> members.id

Table: chats_paralegals
  - chat_id: INTEGER -> chats._id
  - paralegal_id: INTEGER -> paralegals.id

Table: checklist_item_sub_user_assignees
  - checklist_item_id: INTEGER -> checklist_items._id
  - sub_user_id: INTEGER -> sub_users.id

Table: checklist_item_templates
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - firm_id: INTEGER NOT NULL -> firms._id
  - content: TEXT NOT NULL
  - created_by_user_id: INTEGER NOT NULL -> users._id
  - checklist_template_id: INTEGER -> checklist_templates._id
  - position: INTEGER
  - type: TEXT NOT NULL

Table: checklist_items
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - firm_id: INTEGER NOT NULL -> firms._id
  - case_id: INTEGER NOT NULL -> cases._id
  - chat_id: INTEGER NOT NULL -> chats._id
  - sender_id: INTEGER NOT NULL -> users._id
  - created_during_case_status_id: INTEGER NOT NULL -> case_statuses._id
  - checklist_item_template_id: INTEGER -> checklist_item_templates._id
  - automation_template_id: INTEGER -> automation_templates._id
  - sender_child_id: INTEGER NOT NULL
  - sender_type: TEXT NOT NULL
  - new_due_date: TIMESTAMP WITHOUT TIME ZONE
  - content: TEXT NOT NULL
  - completed_date: TIMESTAMP WITHOUT TIME ZONE
  - completed_by_id: INTEGER -> users._id
  - completed_by_child_id: INTEGER
  - completed_by_type: TEXT
  - type: TEXT NOT NULL
  - checklist_completed_message_sent: TIMESTAMP WITHOUT TIME ZONE
  - checklist_created_message_sent: TIMESTAMP WITHOUT TIME ZONE
  - position: INTEGER

Table: checklist_items_messages
  - checklist_item_id: INTEGER -> checklist_items._id
  - message_id: INTEGER -> messages._id

Table: checklist_templates
  - id: INTEGER [PK] NOT NULL
  - created_by_id: INTEGER NOT NULL -> users._id
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - firm_id: INTEGER NOT NULL -> firms._id
  - title: TEXT NOT NULL

Table: clients
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - user_id: INTEGER -> users._id
  - firm_id: INTEGER -> firms._id
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - client_invited_date: TIMESTAMP WITHOUT TIME ZONE
  - birth_date: DATE
  - ssn: BYTEA
  - opt_out: BOOLEAN
  - sent_opt_out_msg: TIMESTAMP WITHOUT TIME ZONE
  - integration_id: TEXT
  - descriptor: TEXT
  - preferred_language: VARCHAR
  - most_recent_message_sent_at: TIMESTAMP WITHOUT TIME ZONE
  - most_recent_notification_read_at: TIMESTAMP WITHOUT TIME ZONE
  - last_digest: TIMESTAMP WITHOUT TIME ZONE
  - wants_daily_digest: BOOLEAN
  - wants_email_notifications: BOOLEAN
  - wants_email_notification_types: TEXT[]

Table: cms_case_statuses
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - name: TEXT
  - firm_id: INTEGER -> firms._id
  - integration_id: TEXT
  - integration_type: TEXT
  - number: INTEGER
  - cms_case_type_id: INTEGER -> cms_case_types._id

Table: cms_case_types
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - name: TEXT
  - firm_id: INTEGER -> firms._id
  - integration_id: TEXT
  - integration_type: TEXT

Table: credentials
  - id: INTEGER [PK] NOT NULL
  - firm_id: INTEGER -> firms._id
  - resource_key: TEXT NOT NULL
  - token: JSON NOT NULL
  - client_id: TEXT
  - client_secret: TEXT
  - access_token: TEXT NOT NULL
  - refresh_token: TEXT NOT NULL
  - expiration: TIMESTAMP WITHOUT TIME ZONE NOT NULL
  - username: TEXT
  - password: BYTEA
  - clio_matter_webhook_id: INTEGER
  - clio_matter_webhook_expiration: TIMESTAMP WITHOUT TIME ZONE
  - clio_cal_webhook_id: INTEGER
  - clio_cal_webhook_expiration: TIMESTAMP WITHOUT TIME ZONE
  - clio_cal_webhook_shared_secret: TEXT
  - clio_matter_webhook_shared_secret: TEXT
  - smokeball_webhook_id: TEXT
  - smokeball_webhook_secret: TEXT
  - mycase_webhook_id: TEXT
  - mycase_webhook_secret: TEXT
  - custom_domain: TEXT
  - api_key: TEXT
  - lock_api_calls: BOOLEAN
  - workflow: TEXT
  - last_used: TIMESTAMP WITHOUT TIME ZONE
  - is_sandbox: BOOLEAN
  - neos_note_topic_id: TEXT
  - callrail_settings: JSONB
  - reauth_date: TIMESTAMP WITHOUT TIME ZONE
  - docuware_file_cabinet_id: TEXT
  - filevine_personal_access_token: TEXT
  - filevine_pat_user_id: TEXT
  - filevine_pat_org_id: TEXT

Table: cs_celery_metrics
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - category: TEXT
  - task_count: INTEGER
  - task_name: TEXT

Table: cs_stream_logs
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - payload: JSONB
  - defunct_payload: TEXT
  - queue_name: TEXT
  - execution_time: FLOAT
  - error_messaging: TEXT
  - stream_type: TEXT
  - case_id: INTEGER -> cases._id
  - firm_id: INTEGER -> firms._id

Table: cs_stream_metrics
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - stream_type: TEXT
  - queue_length: INTEGER
  - queue_name: TEXT

Table: csat_survey_configs
  - id: INTEGER [PK] NOT NULL
  - firm_id: INTEGER -> firms._id
  - case_type_id: INTEGER -> case_types._id
  - is_default: BOOLEAN
  - trigger_on_interval: BOOLEAN
  - trigger_on_stage_change: BOOLEAN
  - interval_days: INTEGER
  - minimum_days_between_surveys: INTEGER
  - prompt: TEXT
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE

Table: csat_surveys
  - id: INTEGER [PK] NOT NULL
  - config_id: INTEGER -> csat_survey_configs.id
  - case_id: INTEGER -> cases._id
  - client_id: INTEGER -> clients.id
  - firm_id: INTEGER -> firms._id
  - case_status_id: INTEGER -> case_statuses._id
  - send_at: TIMESTAMP WITHOUT TIME ZONE NOT NULL
  - sent_at: TIMESTAMP WITHOUT TIME ZONE
  - historical_prompt: TEXT
  - score: INTEGER
  - comment: TEXT
  - trigger_type: trigger_types NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - status: status_types NOT NULL
  - show_to_client: BOOLEAN

Table: custom_brandings
  - id: INTEGER [PK] NOT NULL
  - firm_id: INTEGER -> firms._id
  - organization_id: INTEGER -> organizations._id
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - file_name: TEXT
  - content_type: TEXT
  - random_id: TEXT
  - extension: TEXT
  - branding_color: TEXT
  - heading_color: TEXT
  - content_color: TEXT
  - active_text_highlight: TEXT
  - is_default: BOOLEAN
  - label: TEXT
  - brand_97l: TEXT
  - brand_93l: TEXT
  - brand_88l: TEXT
  - brand_74l: TEXT
  - brand_neg_10l: TEXT
  - brand_neg_20l: TEXT
  - brand_neg_30l: TEXT

Table: development_whitelists
  - id: INTEGER [PK] NOT NULL
  - cell_phone: TEXT
  - email_address: TEXT
  - developer_name: TEXT

Table: document_signatories
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - sub_user_id: INTEGER -> sub_users.id
  - file_id: INTEGER -> files._id
  - order: INTEGER
  - signed_at: TIMESTAMP WITHOUT TIME ZONE
  - signature_input: TEXT
  - prefix: TEXT

Table: feature_audit_logs
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - feature: TEXT
  - value: TEXT
  - user_id: INTEGER -> users._id
  - firm_id: INTEGER -> firms._id

Table: files
  - id: INTEGER [PK] NOT NULL
  - uuid: TEXT
  - case_id: INTEGER -> cases._id
  - firm_id: INTEGER -> firms._id
  - sender_id: INTEGER -> users._id
  - original_document_id: INTEGER -> files._id
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - file_name: TEXT
  - link_expiration: TIMESTAMP WITHOUT TIME ZONE
  - audit_trail: TEXT
  - content_type: TEXT
  - integration_error: TEXT
  - sender_type: TEXT
  - integration_success: BOOLEAN
  - synced_at: TIMESTAMP WITHOUT TIME ZONE
  - synced_by_third_party: BOOLEAN
  - s3_key: TEXT
  - thumbnail_s3_key: TEXT
  - extension: TEXT
  - size: INTEGER
  - received_as_text: BOOLEAN
  - sync_failures: INTEGER
  - template_file: BOOLEAN
  - error_messages: TEXT
  - uploaded_to_s3: BOOLEAN
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE

Table: firm_features
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - partner_portal: BOOLEAN
  - automation: BOOLEAN
  - treatment_log: BOOLEAN
  - checklist: BOOLEAN
  - e_sign: BOOLEAN
  - updated_at: TIMESTAMP WITHOUT TIME ZONE

Table: firm_selection_reasons
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - created_by_id: INTEGER -> users._id
  - firm_id: INTEGER -> firms._id
  - is_default: BOOLEAN
  - reason: TEXT
  - is_hidden: BOOLEAN

Table: firm_selection_responses
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - firm_id: INTEGER -> firms._id
  - client_id: INTEGER -> sub_users.id
  - case_id: INTEGER -> cases._id
  - reason_id: INTEGER -> firm_selection_reasons.id

Table: firm_settings
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - settings: JSONB
  - firm_id: INTEGER -> firms._id
  - organization_id: INTEGER -> organizations._id
  - package: TEXT

Table: firms
  - id: INTEGER [PK] NOT NULL
  - name: TEXT
  - last_import_started: TIMESTAMP WITHOUT TIME ZONE
  - last_import_completed: TIMESTAMP WITHOUT TIME ZONE
  - deactivated: BOOLEAN
  - phone_number_region: TEXT
  - review_link: TEXT
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - hours_start: INTEGER
  - hours_end: INTEGER
  - timezone: TEXT
  - pricing_tier_id: INTEGER -> pricing_tiers._id
  - pricing_model_id: INTEGER -> pricing_models._id
  - invite_link: TEXT
  - include_case_managers: BOOLEAN
  - is_test_account: BOOLEAN
  - implementation_date: DATE
  - dashboard_url: TEXT
  - dashboard_api_log: TEXT
  - dashboard_url_created_at: TIMESTAMP WITHOUT TIME ZONE
  - allow_filevine_webhook_queue: BOOLEAN
  - firm_allow_medical_provider_stream: BOOLEAN
  - firm_allows_checklist_created_stream: BOOLEAN
  - firm_allows_checklist_reminder_stream: BOOLEAN
  - firm_allows_checklist_completed_stream: BOOLEAN
  - orphaned_user_firm: BOOLEAN
  - scout_collection_id: TEXT
  - scout_web_scraping_table_id: TEXT
  - scout_message_templates_table_id: TEXT
  - sitemap_crawled_at: TIMESTAMP WITHOUT TIME ZONE
  - messaging_off: TIMESTAMP WITHOUT TIME ZONE
  - exclude_data_from_models: BOOLEAN
  - website_url: TEXT
  - sitemap_url: TEXT
  - region: TEXT

Table: firms_lead_enrollment
  - id: INTEGER [PK] NOT NULL
  - firm_id: INTEGER NOT NULL -> firms._id
  - is_statusphere_enabled: BOOLEAN NOT NULL
  - statusphere_opt_in_date: TIMESTAMP WITHOUT TIME ZONE
  - practice_areas: TEXT[] NOT NULL
  - referral_networks: TEXT[]
  - recipient_email: TEXT
  - service_areas_zip_codes: JSONB
  - max_referrals_per_month: INTEGER NOT NULL
  - last_lead_received_at: TIMESTAMP WITHOUT TIME ZONE
  - created_by_user_id: INTEGER -> users._id
  - updated_by_user_id: INTEGER -> users._id
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE

Table: form_responses
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - form_id: TEXT
  - chat_id: INTEGER -> chats._id
  - user_id: INTEGER -> users._id
  - firm_id: INTEGER -> firms._id
  - form_response: TEXT
  - organization_notes: TEXT
  - request_notes: TEXT

Table: hubspot_scorecards
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - firm_id: INTEGER -> firms._id
  - activation_score: TEXT
  - activation_percentage: FLOAT
  - engagement_score: TEXT
  - engagement_percentage: FLOAT
  - growth_score: TEXT
  - growth_percentage: FLOAT
  - value_score: TEXT
  - value_percentage: FLOAT
  - audit_trail: TEXT
  - client_logins_total: INTEGER
  - client_logins_last_thirty_days: INTEGER
  - treatments_per_100_cases: FLOAT
  - appointments_per_100_cases: FLOAT
  - automations_per_100_cases: FLOAT
  - checklist_items_per_100_cases: FLOAT
  - messages_per_100_cases: FLOAT
  - documents_per_100_cases: FLOAT

Table: implementation_whitelist
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - firm_id: INTEGER -> firms._id
  - user_id: INTEGER -> users._id

Table: import_logs
  - id: INTEGER [PK] NOT NULL
  - type: TEXT
  - integration_id: TEXT
  - matter_id: TEXT
  - firm_id: INTEGER -> firms._id
  - case_id: INTEGER -> cases._id
  - data: JSON
  - object_dump: JSON
  - error_messaging: TEXT
  - success_messaging: TEXT
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - created: BOOLEAN
  - updated: BOOLEAN
  - failed: BOOLEAN

Table: invoices
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - case_id: INTEGER -> cases._id
  - firm_id: INTEGER NOT NULL -> firms._id
  - receivable: FLOAT
  - receivable_processed: FLOAT
  - receivable_processed_date: TIMESTAMP WITHOUT TIME ZONE
  - receivable_success_message: TEXT
  - receivable_error_message: TEXT
  - payable: FLOAT
  - payable_processed: FLOAT
  - payable_processed_date: TIMESTAMP WITHOUT TIME ZONE
  - payable_success_message: TEXT
  - payable_error_message: TEXT
  - stripe_charge_id: TEXT
  - stripe_receipt_id: TEXT
  - stripe_refund_id: TEXT
  - invoice_category: TEXT NOT NULL
  - process_on_resolution: BOOLEAN NOT NULL
  - process_on_activation: BOOLEAN NOT NULL

Table: lead_routing_attempts
  - id: INTEGER [PK] NOT NULL
  - lead_id: INTEGER NOT NULL -> leads._id
  - firm_id: INTEGER NOT NULL -> firms._id
  - attempt_number: INTEGER NOT NULL
  - attempt_uuid: UUID NOT NULL
  - status: VARCHAR(50)
  - timestamp_sent: TIMESTAMP WITHOUT TIME ZONE
  - timestamp_opened: TIMESTAMP WITHOUT TIME ZONE
  - timestamp_actioned: TIMESTAMP WITHOUT TIME ZONE
  - email_service_message_id: TEXT
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE

Table: leads
  - id: INTEGER [PK] NOT NULL
  - typeform_submission_id: VARCHAR(255)
  - raw_typeform_payload: JSONB
  - status: VARCHAR(50) NOT NULL
  - first_name: TEXT
  - last_name: TEXT
  - email: TEXT
  - phone: TEXT
  - zip_code: VARCHAR(10)
  - practice_area_raw: TEXT
  - practice_area_mapped: VARCHAR(255)
  - description: TEXT
  - urgency: VARCHAR(50)
  - preferred_contact_methods: TEXT[]
  - language: VARCHAR(20)
  - current_routing_attempt_count: INTEGER NOT NULL
  - accepted_by_firm_id: INTEGER -> firms._id
  - manual_review_reason: TEXT
  - internal_notes: TEXT
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE

Table: live_feed_items
  - id: INTEGER [PK] NOT NULL
  - case_id: INTEGER -> cases._id
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - client_id: INTEGER -> clients.id
  - firm_id: INTEGER -> firms._id
  - sender_id: INTEGER -> users._id
  - sender_type: TEXT
  - type: TEXT

Table: matter_imports
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - last_import: TIMESTAMP WITHOUT TIME ZONE
  - excluded_from_import: TIMESTAMP WITHOUT TIME ZONE
  - firm_id: INTEGER -> firms._id
  - case_id: INTEGER -> cases._id
  - readable_id: TEXT
  - integration_id: TEXT
  - case_type_id: INTEGER -> case_types._id
  - case_status_id: INTEGER -> case_statuses._id
  - client_first_name: TEXT
  - client_last_name: TEXT
  - link: TEXT
  - raw_matter: JSONB
  - errors_found: JSONB
  - is_closed: BOOLEAN
  - synthetic_clients_data: JSONB

Table: matter_logs
  - id: INTEGER [PK] NOT NULL
  - integration_id: TEXT
  - readable_id: TEXT
  - firm_id: INTEGER -> firms._id
  - matter_import_file_id: INTEGER -> matter_import_files._id
  - matter_import_id: INTEGER -> matter_imports._id
  - data: JSON
  - error_messaging: TEXT
  - success_messaging: TEXT
  - warning_messaging: TEXT
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - validation: BOOLEAN
  - case_created: BOOLEAN
  - case_updated: BOOLEAN
  - failed: BOOLEAN
  - stack_trace: TEXT
  - bulk_action_id: INTEGER -> bulk_actions._id

Table: medical_providers
  - id: INTEGER [PK] NOT NULL
  - firm_id: INTEGER -> firms._id
  - case_id: INTEGER -> cases._id
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - service_start_date: TIMESTAMP WITHOUT TIME ZONE
  - service_end_date: TIMESTAMP WITHOUT TIME ZONE
  - office_name: TEXT
  - address: TEXT
  - doctor_name: TEXT
  - office_phone_number: TEXT
  - integration_id: TEXT
  - provider_type: TEXT
  - created_by_integration: BOOLEAN

Table: members
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - user_id: INTEGER -> users._id
  - organization_id: INTEGER -> organizations._id
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - descriptor: TEXT
  - last_digest: TIMESTAMP WITHOUT TIME ZONE
  - wants_daily_digest: BOOLEAN
  - wants_email_notifications: BOOLEAN
  - wants_email_notification_types: TEXT[]

Table: message_templates
  - id: INTEGER [PK] NOT NULL
  - title: TEXT
  - is_default: BOOLEAN
  - content: TEXT
  - created_at: DATE
  - updated_at: DATE
  - template_type: TEXT
  - type_access: TEXT
  - firm_id: INTEGER -> firms._id
  - created_by_id: INTEGER -> users._id
  - updated_by_id: INTEGER -> users._id
  - file_attachment_id: INTEGER -> files._id
  - is_system: BOOLEAN
  - shortcodes_not_supported: BOOLEAN

Table: messages
  - id: INTEGER [PK] NOT NULL
  - case_id: INTEGER -> cases._id
  - has_logged_treatment: BOOLEAN
  - checklist_item_id: INTEGER -> checklist_items._id
  - treatment_id: INTEGER -> appointments._id
  - status_number: INTEGER
  - content: TEXT
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - sent_at: TIMESTAMP WITHOUT TIME ZONE
  - scheduled_message_send_date: TIMESTAMP WITHOUT TIME ZONE
  - scheduled_message_sent_date: TIMESTAMP WITHOUT TIME ZONE
  - synced_at: TIMESTAMP WITHOUT TIME ZONE
  - synced_by_third_party: BOOLEAN
  - integration_error: TEXT
  - internal_integration_error: TEXT
  - sender_id: INTEGER -> users._id
  - sender_child_id: INTEGER
  - sender_type: TEXT
  - sender_name: TEXT
  - is_automated_defunct: BOOLEAN
  - automated_message_type: TEXT
  - automation_id: INTEGER -> automations._id
  - scheduled_invite: BOOLEAN
  - type: TEXT
  - message_template_type: TEXT
  - received_as_text: BOOLEAN
  - sms_errors: TEXT[]
  - retried_at: TIMESTAMP WITHOUT TIME ZONE
  - integration_id: TEXT
  - firm_id: INTEGER -> firms._id
  - original_content: TEXT
  - translated_content: TEXT
  - target_language: TEXT
  - review_sent: BOOLEAN
  - invite_sent: BOOLEAN
  - translation_edited: BOOLEAN
  - translation_source: TEXT
  - bulk_action_id: INTEGER -> bulk_actions._id
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - contains_question: BOOLEAN
  - source: TEXT
  - recommended_response_requested: TIMESTAMP WITHOUT TIME ZONE
  - recommended_response_used_id: INTEGER -> recommended_responses._id
  - language: TEXT
  - urgency: INTEGER
  - complexity: INTEGER
  - sentiment: FLOAT
  - target_sentiment: INTEGER
  - category: TEXT
  - subcategory: TEXT
  - classification_retried_at: TIMESTAMP WITHOUT TIME ZONE
  - system_message_metadata: JSONB
  - primary_attorney_id_at_send: INTEGER -> attorneys.id

Table: messages_files
  - id: INTEGER
  - message_id: INTEGER -> messages._id
  - file_id: INTEGER -> files._id
  - created_at: TIMESTAMP WITHOUT TIME ZONE

Table: net_promoter_score_reports
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - case_id: INTEGER -> cases._id
  - client_id: INTEGER -> clients.id
  - firm_id: INTEGER -> firms._id
  - nps_feedback: TEXT
  - nps_id: INTEGER -> net_promoter_scores._id
  - nps_score: INTEGER
  - nps_updated_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE

Table: net_promoter_scores
  - id: INTEGER [PK] NOT NULL
  - case_id: INTEGER -> cases._id
  - firm_id: INTEGER -> firms._id
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - stage_1: INTEGER
  - updated_at_1: TIMESTAMP WITHOUT TIME ZONE
  - stage_2: INTEGER
  - updated_at_2: TIMESTAMP WITHOUT TIME ZONE
  - stage_3: INTEGER
  - updated_at_3: TIMESTAMP WITHOUT TIME ZONE
  - stage_4: INTEGER
  - updated_at_4: TIMESTAMP WITHOUT TIME ZONE
  - stage_5: INTEGER
  - updated_at_5: TIMESTAMP WITHOUT TIME ZONE
  - stage_6: INTEGER
  - updated_at_6: TIMESTAMP WITHOUT TIME ZONE
  - stage_7: INTEGER
  - updated_at_7: TIMESTAMP WITHOUT TIME ZONE
  - stage_8: INTEGER
  - updated_at_8: TIMESTAMP WITHOUT TIME ZONE
  - stage_9: INTEGER
  - updated_at_9: TIMESTAMP WITHOUT TIME ZONE
  - stage_10: INTEGER
  - updated_at_10: TIMESTAMP WITHOUT TIME ZONE
  - stage_11: INTEGER
  - updated_at_11: TIMESTAMP WITHOUT TIME ZONE
  - stage_12: INTEGER
  - updated_at_12: TIMESTAMP WITHOUT TIME ZONE
  - feedback_stage_1: TEXT
  - feedback_stage_2: TEXT
  - feedback_stage_3: TEXT
  - feedback_stage_4: TEXT
  - feedback_stage_5: TEXT
  - feedback_stage_6: TEXT
  - feedback_stage_7: TEXT
  - feedback_stage_8: TEXT
  - feedback_stage_9: TEXT
  - feedback_stage_10: TEXT
  - feedback_stage_11: TEXT
  - feedback_stage_12: TEXT
  - client_id: INTEGER -> clients.id
  - current_status_number: INTEGER
  - most_recent_nps: INTEGER

Table: notifications
  - id: INTEGER [PK] NOT NULL
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - case_id: INTEGER -> cases._id
  - content: TEXT
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - message_id: INTEGER -> messages._id
  - read_at: TIMESTAMP WITHOUT TIME ZONE
  - sender_name: TEXT
  - recipient_name: TEXT
  - sent_as_text: BOOLEAN
  - delivered_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - user_id: INTEGER -> users._id
  - is_automated_defunct: BOOLEAN
  - automated_message_type: TEXT
  - child_id: INTEGER
  - user_type: TEXT
  - sms_error: TEXT
  - audit_trail: TEXT
  - sms_content: TEXT
  - read_by_id: INTEGER -> sub_users.child_id
  - unread_at: TIMESTAMP WITHOUT TIME ZONE
  - firm_id: INTEGER -> firms._id
  - sending_number: TEXT
  - sender_child_id: INTEGER
  - sender_type: TEXT
  - email_sent_at: TIMESTAMP WITHOUT TIME ZONE
  - email_delivered_at: TIMESTAMP WITHOUT TIME ZONE
  - email_interacted_type: TEXT
  - email_interacted_at: TIMESTAMP WITHOUT TIME ZONE
  - email_unique_token: TEXT
  - read_by_sub_user_id: INTEGER -> sub_users.id

Table: nps_predictions
  - id: INTEGER [PK] NOT NULL
  - case_id: INTEGER -> cases._id
  - firm_id: INTEGER -> firms._id
  - detractor_probability: FLOAT
  - approval: BOOLEAN
  - approval_sub_user_id: INTEGER -> sub_users.id
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE

Table: organizations
  - id: INTEGER [PK] NOT NULL
  - name: TEXT
  - trial_expired: BOOLEAN
  - phone_number: TEXT
  - phone_number_region: TEXT
  - about: TEXT
  - descriptor: TEXT
  - feature_funding: BOOLEAN
  - feature_record_retrieval: BOOLEAN
  - form_id: TEXT

Table: organizations_firms
  - firm_id: INTEGER -> firms._id
  - organization_id: INTEGER -> organizations._id

Table: paralegals
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - user_id: INTEGER -> users._id
  - firm_id: INTEGER -> firms._id
  - business_number: TEXT
  - contact_email_address: TEXT
  - bio: TEXT
  - wants_sms: BOOLEAN
  - send_as_primary: BOOLEAN
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - integration_id: TEXT
  - descriptor: TEXT
  - case_notifications_off: BOOLEAN
  - last_digest: TIMESTAMP WITHOUT TIME ZONE
  - wants_daily_digest: BOOLEAN
  - wants_ics_invites: BOOLEAN
  - calendar_type: calendar_types
  - wants_exception_reporting: BOOLEAN
  - wants_email_notifications: BOOLEAN
  - wants_email_notification_types: TEXT[]
  - receive_unknown_client_notification: BOOLEAN
  - preferences: JSONB
  - onboarding_seen: TEXT[]

Table: practice_area_mapping
  - id: INTEGER [PK] NOT NULL
  - related_area: TEXT NOT NULL
  - main_area: TEXT NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE

Table: practice_area_templates
  - id: INTEGER [PK] NOT NULL
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - name: TEXT

Table: pricing_models
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - name: TEXT NOT NULL
  - charge_frequency: TEXT NOT NULL
  - resolution_period: INTEGER
  - trigger_type: TEXT
  - case_receivable_cap: FLOAT
  - activation_fee: FLOAT
  - monthly_fee: FLOAT
  - resolution_fee: FLOAT
  - refund_before_thirty_days: BOOLEAN
  - description: TEXT

Table: pricing_tiers
  - id: INTEGER [PK] NOT NULL
  - firm_feature_id: INTEGER -> firm_features._id
  - package: TEXT
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - level: INTEGER
  - updated_at: TIMESTAMP WITHOUT TIME ZONE

Table: product_implementations
  - id: INTEGER [PK] NOT NULL
  - firm_id: INTEGER NOT NULL -> firms._id
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - last_url_visited: TEXT
  - onboarding_state: JSONB
  - version: FLOAT NOT NULL

Table: profile_pictures
  - id: INTEGER [PK] NOT NULL
  - content_type: TEXT
  - extension: TEXT
  - user_id: INTEGER -> users._id
  - size: INTEGER
  - folder: TEXT
  - s3_key: TEXT
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE

Table: recommended_responses
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - content: TEXT
  - final_content: TEXT
  - firm_id: INTEGER -> firms._id
  - case_id: INTEGER -> cases._id
  - message_id: INTEGER -> messages._id
  - category: TEXT
  - approved: BOOLEAN
  - instructions: TEXT
  - ai_transaction_id: INTEGER
  - batch_id: UUID
  - unanswered_messages_summary: TEXT

Table: responses
  - id: INTEGER [PK] NOT NULL
  - case_id: INTEGER -> cases._id
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - client_id: INTEGER -> clients.id
  - firm_id: INTEGER -> firms._id
  - attorney_id: INTEGER -> attorneys.id
  - new_message_id: INTEGER -> messages._id
  - last_message_id: INTEGER -> messages._id
  - response_time: INTEGER
  - type: TEXT

Table: sisense_group_mappings
  - id: INTEGER [PK] NOT NULL
  - firm_id: INTEGER NOT NULL -> firms._id
  - sisense_group_id: VARCHAR(255) NOT NULL
  - group_name: VARCHAR(255) NOT NULL
  - dashboard_type: VARCHAR(50) NOT NULL
  - dashboard_id: VARCHAR(255)
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE

Table: sisense_user_group_access
  - id: INTEGER [PK] NOT NULL
  - user_id: INTEGER NOT NULL -> users._id
  - sub_user_id: INTEGER NOT NULL -> sub_users.id
  - firm_id: INTEGER NOT NULL -> firms._id
  - sisense_group_id: VARCHAR(255) NOT NULL
  - sisense_group_mapping_id: INTEGER NOT NULL -> sisense_group_mappings.id
  - granted_by_user_id: INTEGER -> users._id
  - granted_by_sub_user_id: INTEGER -> sub_users.id
  - granted_at: TIMESTAMP WITHOUT TIME ZONE
  - revoked_at: TIMESTAMP WITHOUT TIME ZONE
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE

Table: sisense_user_mappings
  - id: INTEGER [PK] NOT NULL
  - user_id: INTEGER NOT NULL -> users._id
  - sub_user_id: INTEGER NOT NULL -> sub_users.id
  - sisense_user_id: VARCHAR(255) NOT NULL
  - email_address: VARCHAR(255) NOT NULL
  - role: VARCHAR(255) NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE

Table: sms_integrations
  - id: INTEGER [PK] NOT NULL
  - firm_id: INTEGER -> firms._id
  - account_id: TEXT NOT NULL
  - auth_key: BYTEA NOT NULL
  - subaccount_id: TEXT
  - subaccount_name: TEXT NOT NULL
  - subaccount_auth: BYTEA
  - phone_number: TEXT NOT NULL
  - segments_per_second: INTEGER
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - custom_authentication_service: BOOLEAN
  - tollfree_phone_number_sid: TEXT
  - tollfree_registration_sid: TEXT
  - broker_type: TEXT
  - tollfree_registration_status: TEXT
  - tollfree_registration_status_last_requested: TIMESTAMP WITHOUT TIME ZONE
  - is_default: BOOLEAN

Table: sms_integrations_case_types
  - sms_integration_id: INTEGER -> sms_integrations._id
  - case_type_id: INTEGER -> case_types._id

Table: stage_placements
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - content: TEXT
  - final_content: TEXT
  - firm_id: INTEGER -> firms._id
  - category: TEXT
  - category_value: TEXT
  - approved: BOOLEAN
  - instructions: TEXT
  - ai_transaction_id: INTEGER -> ai_transactions._id

Table: stripe_integrations
  - id: INTEGER [PK] NOT NULL
  - firm_id: INTEGER -> firms._id
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - customer_id: TEXT
  - subscription_id: TEXT

Table: sub_users
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - user_id: INTEGER -> users._id
  - child_id: INTEGER
  - firm_id: INTEGER -> firms._id
  - organization_id: INTEGER -> organizations._id
  - user_permission_id: INTEGER -> user_permissions._id
  - type: TEXT
  - descriptor: TEXT
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - client_invited_date: TIMESTAMP WITHOUT TIME ZONE
  - birth_date: DATE
  - ssn: BYTEA
  - opt_out: BOOLEAN
  - sent_opt_out_msg: TIMESTAMP WITHOUT TIME ZONE
  - integration_id: TEXT
  - most_recent_message_sent_at: TIMESTAMP WITHOUT TIME ZONE
  - most_recent_notification_read_at: TIMESTAMP WITHOUT TIME ZONE
  - wants_daily_digest: BOOLEAN
  - business_number: TEXT
  - contact_email_address: TEXT
  - bio: TEXT
  - wants_sms: BOOLEAN
  - case_notifications_off: BOOLEAN
  - wants_ics_invites: BOOLEAN
  - calendar_type: calendar_types

Table: treatment_activities
  - id: INTEGER [PK] NOT NULL
  - appointment_id: INTEGER -> appointments._id
  - child_id: INTEGER
  - user_id: INTEGER -> users._id
  - user_type: TEXT
  - action: TEXT
  - fields_updated: TEXT
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE

Table: treatment_types
  - id: INTEGER [PK] NOT NULL
  - name: TEXT

Table: triage_assignees
  - sub_user_id: INTEGER [PK] NOT NULL -> sub_users.id
  - triage_record_id: INTEGER [PK] NOT NULL -> triage_records._id
  - created_at: TIMESTAMP WITHOUT TIME ZONE NOT NULL
  - updated_at: TIMESTAMP WITHOUT TIME ZONE NOT NULL

Table: triage_records
  - id: INTEGER [PK] NOT NULL
  - case_id: INTEGER NOT NULL -> cases._id
  - firm_id: INTEGER NOT NULL -> firms._id
  - snoozed_by: INTEGER -> users._id
  - triage_score: FLOAT
  - snoozed_until: TIMESTAMP WITHOUT TIME ZONE
  - resolved_at: TIMESTAMP WITHOUT TIME ZONE
  - locked_until: TIMESTAMP WITHOUT TIME ZONE
  - suppressed_until: TIMESTAMP WITHOUT TIME ZONE
  - unanswered_client_messages: INTEGER
  - overdue_tasks: INTEGER
  - missing_treatment_logs: INTEGER
  - appointments_missing_confirmation: INTEGER
  - low_staff_activity: BOOLEAN
  - case_on_hold: BOOLEAN
  - phone_connection_issues: BOOLEAN
  - approval: BOOLEAN
  - message_intent: TEXT
  - feedback: TEXT NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE NOT NULL
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - hashed_payload: TEXT
  - last_processed_timestamp: TIMESTAMP WITHOUT TIME ZONE

Table: user_logins
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - user_id: INTEGER -> users._id
  - device_type: TEXT
  - user_type: TEXT
  - firm_id: INTEGER -> firms._id
  - organization_id: INTEGER -> organizations._id

Table: user_permissions
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - settings: JSON
  - name: TEXT
  - permissions_type: TEXT
  - firm_id: INTEGER -> firms._id
  - organization_id: INTEGER -> organizations._id

Table: user_two_fa_configurations
  - user_id: BIGINT [PK] NOT NULL -> users._id
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - updated_at: TIMESTAMP WITHOUT TIME ZONE

Table: users
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - first_name: TEXT
  - last_name: TEXT
  - email_address: TEXT
  - cell_phone: TEXT
  - last_opened: TIMESTAMP WITHOUT TIME ZONE
  - password_reset_token: CHAR(55)
  - password_reset_token_expiration: INTEGER
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - device_token: TEXT
  - device_type: TEXT
  - device_endpoint: TEXT
  - login_verification_code: TEXT
  - login_verification_code_expiration: TIMESTAMP WITHOUT TIME ZONE
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - mobile_app_version: TEXT
  - mobile_os_version: TEXT
  - mobile_screen_size: TEXT
  - user_language: TEXT
  - google_oauth_credential: JSON
  - google_calendar_id: TEXT
  - app_update_notification_processed: TIMESTAMP WITHOUT TIME ZONE
  - app_update_notification_processed_audit: TEXT
  - last_used_web_app: TIMESTAMP WITHOUT TIME ZONE
  - last_used_ios_app: TIMESTAMP WITHOUT TIME ZONE
  - last_used_android_app: TIMESTAMP WITHOUT TIME ZONE
  - created_by_attempted_login: BOOLEAN

Table: videos
  - id: INTEGER [PK] NOT NULL
  - firm_id: INTEGER -> firms._id
  - updated_by_user_id: INTEGER -> users._id
  - updated_by_sub_user_id: INTEGER -> sub_users.id
  - updated_at: TIMESTAMP WITHOUT TIME ZONE
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - filename: TEXT
  - link_expiration: TIMESTAMP WITHOUT TIME ZONE
  - title: TEXT
  - source: TEXT
  - aspect_ratio: TEXT
  - s3_key: TEXT
  - thumbnail_s3_key: TEXT
  - extension: TEXT
  - size: INTEGER
  - thumbnail_url: TEXT

Table: vitally_scorecards
  - id: INTEGER [PK] NOT NULL
  - created_at: TIMESTAMP WITHOUT TIME ZONE
  - deleted_at: TIMESTAMP WITHOUT TIME ZONE
  - firm_id: INTEGER NOT NULL
  - user_id: INTEGER
  - user_first_last_name: TEXT
  - user_case_type: TEXT
  - user_metric_ranking: INTEGER
  - user_case_id: INTEGER
  - period_year: INTEGER
  - period_month: INTEGER
  - metric_name: TEXT NOT NULL
  - metric_value: FLOAT

