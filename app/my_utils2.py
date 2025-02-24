from weasyprint import HTML
import os
from datetime import datetime
import requests
from dotenv import load_dotenv
from app.office365_api import SharePoint

load_dotenv()

# Informations d'authentification
KOBO_USERNAME = os.getenv("KOBO_USERNAME")
KOBO_PASSWORD = os.getenv("KOBO_PASSWORD")
KOBO_AUTH = (KOBO_USERNAME, KOBO_PASSWORD)

def create_pdf_from_data(data):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(current_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pdf_file_path = os.path.join(current_dir, f"output_{date_str}.pdf")

    # Embed CSS directly into the HTML content
    css_content = """
    body {
        font-family: 'Helvetica', Arial, sans-serif;
        margin: 40px;
        background-color: #f9f9f9;
        color: #333;
    }
    h1 {
        color: #333;
        text-align: center;
        border-bottom: 2px solid #333;
        padding-bottom: 10px;
    }
    p {
        font-size: 14px;
        line-height: 1.5;
        margin: 10px 0;
    }
    .label {
        font-weight: bold;
        color: #555;
    }
    .value {
        color: #333;
        padding-left: 20px;
    }
    .section {
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 10px;
        color: #555;
    }
    .photo {
        text-align: center;
        margin: 20px 0;
    }
    img {
        max-width: 100%;
        height: auto;
        border: 1px solid #ddd;
        padding: 5px;
        background-color: #fff;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
    }
    th, td {
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }
    th {
        background-color: #f2f2f2;
    }
    .header, .footer {
        width: 100%;
        text-align: center;
        position: fixed;
    }
    .header {
        top: 0px;
    }
    .footer {
        bottom: 0px;
        font-size: 12px;
        color: #777;
    }
    .page-number:before {
        content: counter(page);
    }
    """

    # Create HTML content
    html_content = f"""
    <html>
    <head>
        <style>
            {css_content}
        </style>
    </head>
    <body>
        <h1>Form Submission</h1>
    """

    # Process JSON data to generate HTML content
    html_content += process_json_data(data, images_dir)

    # Add additional information section
    html_content += f"""
    </body>
    </html>
    """

    # Generate PDF
    try:
        HTML(string=html_content).write_pdf(pdf_file_path)
        print(f"PDF saved at: {pdf_file_path}")
    except Exception as e:
        print(f"Error generating PDF: {e}")


    # Upload PDF to SharePoint
    try:
        upload_to_sharepoint(pdf_file_path)
    except Exception as e:
        print(f"Error uploading PDF to SharePoint: {e}")


    return pdf_file_path

def upload_to_sharepoint(file_path):
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as file:
        file_content = file.read()

    sharepoint = SharePoint()
    response = sharepoint.upload_file(file_name, '', file_content)
    print(f"File uploaded to SharePoint: {response.serverRelativeUrl}")

# =====================================changed ====================================
def process_json_data(data, images_dir):
    # Extract image URLs from attachments
    image_urls = extract_image_urls(data.get('_attachments', []))
    
    html_content = ""
    for key, value in data.items():
        if (key.startswith('site_group/i') and len(key) == 14) or (key.startswith('batiment_group/i') and len(key) == 18) or (key.startswith('electricite_group/i') and len(key) == 22) or (key.startswith('electricite_group/i') and len(key) == 21) or (key.startswith('info_compl/i') and len(key) == 15):
            # Add a description before the image
            description = ""
            if (key.startswith('site_group/i') and len(key) == 14):
                description = "photo contraintes"
            
            # batiment

            elif (key.startswith('batiment_group/i2') and len(key) == 18):
                description = "Vues pignon et long pan"
            elif (key.startswith('batiment_group/i3') and len(key) == 18):
                description = "Accès engins en peripherie : photos"
            elif (key.startswith('batiment_group/i4') and len(key) == 18):
                description = "photo charpente"
            elif (key.startswith('batiment_group/i5') and len(key) == 18):
                description = "photo exterieur et interieur de la couverture"
            elif (key == "batiment_group/i61"):
                description = "photo interieurs du bâtiments"
            elif (key.startswith('batiment_group/i6') and key != "batiment_group/i61"  and len(key) == 18):
                description = "photo exterieur et interieur de la couverture"
            elif (key == "batiment_group/i71"):
                description = "photo(s) montrant l'insertion du projet dans son environnement proche"
            elif (key.startswith('batiment_group/i7') and key != "batiment_group/i71"  and len(key) == 18):
                description = "photo exterieur et interieur de la couverture"
            elif (key == "batiment_group/i81"):
                description = "photo(s) montrant l'insertion du projet dans son environnement lointain"
            elif (key.startswith('batiment_group/i8') and key != "batiment_group/i81"  and len(key) == 18):
                description = "photo exterieur et interieur de la couverture"


            #electricite_group

            elif (key == "electricite_group/i9" and len(key) == 21):
                description = "masque proche (ombreage): photo/ video de l'environnement proche"
            elif (key == "electricite_group/i101"):
                description = "photos des emplacements potentiels"
            elif (key == "electricite_group/i111"):
                description = "Photo TGBT existant"
            elif (key == "electricite_group/i121"):
                description = "Transformateur existant (public, prive): photo"
            elif (key == "electricite_group/i131"):
                description = "Transformateur existant (public, prive) : plaque ou fiche technique"
            elif (key.startswith('electricite_group/i') and  key != "electricite_group/i91" and key != "electricite_group/i101" and key != "electricite_group/i111"and key != "electricite_group/i121"  and key != "electricite_group/i131" and len(key) == 22):
                description = "additionnal image"

            # for information complaimentaire
            elif (key == "info_compl/i141"):
                description = "Contrat d'electricite (si besoin, pour chaque PdL)"
            elif key == "info_compl/i151":
                description = "Facture electrique (pour le calcul des taxes)"
            elif key == "info_compl/i161":
                description = "Autorisation Enedis de collecte des donnees de consommation"
            elif key == "info_compl/i171":
                description = "Indication sur le profil de consommation, les evolutions possibles futures"
            elif (key.startswith('info_compl/i1') and  key != "info_compl/i141" and key != "info_compl/i151" and key != "info_compl/i161"and key != "info_compl/i171" and len(key) == 15):
                description = "additionnal image"

            

            # Add more conditions for other keys as needed
            html_content += f'<p>{description}</p>'
            html_content += process_image(image_urls, value, images_dir)
        elif (key.startswith('site_group/g') and len(key) == 14) or (key.startswith('batiment_group/g') and len(key) == 18) or (key.startswith('electricite_group/g') and (len(key) == 22 or len(key) == 21)) or (key.startswith('info_compl/g') and len(key) == 15):
            html_content += process_geolocation(value)
        else:
            html_content += process_generic_data(key, value)
    return html_content





#####################=======================#################################



def extract_image_urls(attachments):
    image_urls = {}
    for attachment in attachments:
        filename = os.path.basename(attachment.get('filename', '').split('/')[-1])
        download_url = attachment.get('download_url', '')
        print(f"Extracted filename: {filename}, download_url: {download_url}")  # Debugging print
        if filename and download_url:
            # Normalize the filename by replacing spaces with underscores
            normalized_filename = filename.replace(' ', '_')
            image_urls[normalized_filename] = download_url
    return image_urls

def process_image(image_urls, image_name, images_dir):
    # Normalize the image name by replacing spaces with underscores
    normalized_image_name = image_name.replace(' ', '_')
    # Get the image URL from the extracted image URLs
    image_url = image_urls.get(normalized_image_name, "default_image_url")
    print(f"Processing image: {image_name}, URL: {image_url}")  # Debugging print

    # Authenticate and fetch the image URL
    image_url = authenticate_and_get_image_url(image_url)
    print(f"Authenticated image URL: {image_url}")  # Debugging print

    # Download the image locally
    local_image_path = os.path.join(images_dir, normalized_image_name)
    try:
        response = requests.get(image_url, auth=KOBO_AUTH)
        if response.status_code == 200:
            with open(local_image_path, 'wb') as f:
                f.write(response.content)
            print(f"Image downloaded to: {local_image_path}")  # Debugging print
        else:
            print(f"Failed to download image: {image_url}")  # Debugging print
    except Exception as e:
        print(f"Error downloading image: {e}")  # Debugging print

    # Generate HTML for image using the local path
    return f'<div class="photo"><img src="file:///{local_image_path}" alt="Image"></div>'

def authenticate_and_get_image_url(image_url):
    # Authenticate and fetch the image URL
    response = requests.get(image_url, auth=KOBO_AUTH)
    if response.status_code == 200:
        return image_url
    return "default_image_url"

def process_geolocation(geolocation):
    # Generate HTML for geolocation
    return f'<p>Geolocation: {geolocation}</p>'

def process_generic_data(key, value):
    # Generate HTML for generic data
    label = ""
    if key == "site_group/adresse":
        label = "Adresse du site"
    elif key == "site_group/contr_reglem":
        label = "Contraintes d'intervention (horaires, saisons) :"
    elif key == "site_group/is_PL_acces":
        label = "Accès PL, vehicule de chantier :"
    elif key == "site_group/contr_reglem_001":
        label = "Contraintes: lignes HTA existante, réseau:"
    elif (key.startswith('site_group/c') and len(key) == 14):
        label = "commentaire"

    # for batiment group
    elif (key == "batiment_group/info_bati"):
        label = "Information sur les batiments: Age , plans/DOE à disposition/"
    elif (key.startswith("batiment_group/c") and len(key) == 18):
        label = "commentaire"
    elif (key == "batiment_group/d_pign_lpan"):
        label = "Dimensions pignons et longpan:"
    elif (key == "batiment_group/hbp_hf"):
        label = "hauteur baas de pente, hauteur faitage (mesure):"
    elif (key == "batiment_group/t_secu_EPI"):
        label = "type de securisation (EPI) echaufaudage, garde-sorps etc"
    elif (key == "batiment_group/T_charpente"):
        label = "Type de charpente"
    elif (key == "batiment_group/P_charpente"):
        label = "Type de pannes, dimensions des pannes et dimensions(s) des entraxes (important)"
    elif (key == "batiment_group/M_couver"):
        label = "materiau, isolation de la couverture"
    elif (key == "batiment_group/R_couver"):
        label = "reference du materiau de couverture(marque, modèle)"
    elif (key == "batiment_group/d_couver"):
        label = "dimension du materiau de couverture, si applicable - important"
    elif (key == "batiment_group/c_inter"):
        label = "contraintes accès interieur du bâti durant le chantier:"
    elif (key == "batiment_group/renov_gener"):
        label = "Renovation: Observation generales: corrosion, humidite, etancheite etc.."
    elif (key == "batiment_group/renov_attendus"):
        label = "preciser les travaux attendus pour la renovation (desamintage, desenfumage, translucide etc"
  
    # for electricite_group
    elif (key == "electricite_group/t_ombra"):
        label = "masque proche (ombreage): position et dimension (approx.) des obstacles"
    elif (key == "electricite_group/s91"):
        label = "voulez vous ajoutez d'autres photo?"
    elif (key == "electricite_group/racc_indi"):
        label = "ACI / raccordement indirect ?"
    elif (key.startswith("electricite_group/c") and (len(key) == 22 or len(key) == 21)):
        label = "commentaire"
    elif (key.startswith("electricite_group/s") and (len(key) == 22 or len(key) == 21)):
        label = "voulez vous ajoutez d'autres photo?"

    elif (key == "electricite_group/pass_dc"):
        label = "passage DC, descentes de chemin de cables"


    elif (key == "electricite_group/pass_AC"):
        label = "passage des câbles AC jusqu'au TGBT (ACI) ou PDL à creer (VT), nature des revêtement à traverse"
    elif (key == "electricite_group/cat_compteur"):
        label = "Categorie du compteur existant (C1 à C5), puissance de raccordement actuelle"
    elif (key == "electricite_group/dim_arr_elec"):
        label = "Dimensionnement de l'arrivee electricite existante (materiau, section)"
    elif (key == "electricite_group/s131"):
        label = "passage DC, descentes de chemin de cables"


# for Informations complémentaires
    elif (key.startswith("info_compl/c") and len(key) == 15):
        label = "commentaire"
    elif (key.startswith("info_compl/s") and len(key) == 15):
        label = "voulez vous ajoutez d'autres photo?"

    else:
        label = key
    return f'<p><div class="label">{label}:</div> <div class="value">{value}</div></p><br>' \
        if (key != "_attachments" and key != "_geolocation" and (not (key.startswith("batiment_group/s") and len(key) == 18)) \
            and (not (key.startswith("site_group/s") and len(key) == 14)) \
            and (not (key.startswith("electricite_group/s") and (len(key) == 22 or len(key) == 21))) \
            and (not (key.startswith("info_compl/s") and len(key) == 15))) else ""
