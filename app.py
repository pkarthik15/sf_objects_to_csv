from salesforce import Salesforce

sf = Salesforce(
        environment="production", # production | sandbox
        username="",
        password="", # password with security token
        client_id="",
        client_secret=""
    )
sf.get_object_data_using_query(
    query="""SELECT Id, ConvertedAccountId, ConvertedContactId, ConvertedOpportunityId, CreatedById, Email, HasOptedOutOfEmail, IndividualId, LastModifiedById, MasterRecordId FROM Lead WHERE Center_Country__c = 'United States' AND IsConverted = false AND ((Most_Recent_Inquiry_Date__c >= N_DAYS_AGO:550 AND HasOptedOutOfEmail = false) OR Receiving_Promotional_Text__c = true) LIMIT 5000""",
    object_name="Lead"
)