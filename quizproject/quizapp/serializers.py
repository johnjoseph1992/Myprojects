class SchoolSerializer(serializers.ModelSerializer):
    """
    Serializing all the Schools
    """
    class Meta:
        model = School
        fields = ('schoolid', 'schoolname')