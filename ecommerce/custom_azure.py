from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'mytechmediastorage'
    account_key = '11kj/yMi6QvefDc9LQFCSX+KjG1/3w98BsJ/Ntxgqu7U8C42jrvfNRoFoDlj7ZAkCr++WMwyUb1bwbaq598rwg=='
    azure_container = 'media'
    expiration_sec = None
