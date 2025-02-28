from app.office365_api import SharePoint

if (__name__) == "__main__":
    sharepoint = SharePoint()

    print(sharepoint.get_folder_info("Documents"))
