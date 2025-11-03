from rest_framework import serializers

class PatientDataSerializer(serializers.Serializer):
    """
    Serializes the input patient data for the prediction model.
    """
    age_at_diagnosis = serializers.FloatField()
    neoplasm_histologic_grade = serializers.IntegerField()
    her2_status = serializers.CharField()
    er_status = serializers.CharField()
    pr_status = serializers.CharField()
    tumor_size = serializers.FloatField()
    tumor_stage = serializers.IntegerField()
    lymph_nodes_examined_positive = serializers.IntegerField()
    mutation_count = serializers.IntegerField()
    nottingham_prognostic_index = serializers.FloatField()
    inferred_menopausal_state = serializers.CharField()
    brca1 = serializers.FloatField()
    brca2 = serializers.FloatField()
    tp53 = serializers.FloatField()
    erbb2 = serializers.FloatField()
    esr1 = serializers.FloatField()
    pgr = serializers.FloatField()
    akt1 = serializers.FloatField()
    pik3ca = serializers.FloatField()
    mki67 = serializers.FloatField()
    cdh1 = serializers.FloatField()

    def validate_her2_status(self, value):
        if value not in ["Positive", "Negative"]:
            raise serializers.ValidationError("HER2 Status must be 'Positive' or 'Negative'.")
        return value

    def validate_er_status(self, value):
        if value not in ["Positive", "Negative"]:
            raise serializers.ValidationError("ER Status must be 'Positive' or 'Negative'.")
        return value

    def validate_pr_status(self, value):
        if value not in ["Positive", "Negative"]:
            raise serializers.ValidationError("PR Status must be 'Positive' or 'Negative'.")
        return value

    def validate_inferred_menopausal_state(self, value):
        if value not in ["Post", "Pre"]:
            raise serializers.ValidationError("Inferred Menopausal State must be 'Post' or 'Pre'.")
        return value
