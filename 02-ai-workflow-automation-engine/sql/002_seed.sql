INSERT INTO workflow_metrics (metric_name, metric_value, metric_unit)
VALUES
    ('phase_1_placeholder_intake_count', 0, 'count'),
    ('phase_1_placeholder_hours_saved', 0, 'hours')
ON CONFLICT DO NOTHING;
