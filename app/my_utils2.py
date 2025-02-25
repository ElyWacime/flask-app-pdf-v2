from weasyprint import HTML
import os
from datetime import datetime
import requests
from dotenv import load_dotenv
from app.office365_api import SharePoint
from app.somaire import sommaire
from app.css_content import css_content

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

    # Create HTML content
    html_content = f"""
    <html>
    <head>
        <style>
            {css_content}
        </style>
    </head>
    <body>
        {sommaire}
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
            html_content += f'<p><div class="description">{description}</div></p>'
            html_content += process_image(image_urls, value, images_dir)
        elif (key.startswith('site_group/g') and len(key) == 14) or (key.startswith('batiment_group/g') and len(key) == 18) or (key.startswith('electricite_group/g') and (len(key) == 22 or len(key) == 21)) or (key.startswith('info_compl/g') and len(key) == 15):
            html_content += process_geolocation(value)
        else:
            html_content += process_generic_data(key, value)
    return html_content



def process_generic_data(key, value):
    # Generate HTML for generic data
    label = ""
    section_name = ""
    anchor_name = ""

    if key.startswith("site_group"):
        section_name = "Site Group"
        anchor_name = "site_group"
        if key == "site_group/adresse":
            label = "1.1 Adresse du site"
            anchor_name = "site_group/adresse"
        elif key == "site_group/contr_reglem":
            label = "1.2 Contraintes d'intervention (horaires, saisons) :"
            anchor_name = "site_group/contr_reglem"
        elif key == "site_group/is_PL_acces":
            label = "1.3 Accès PL, vehicule de chantier :"
            anchor_name = "site_group/is_PL_acces"
        elif key == "site_group/contr_reglem_001":
            label = "1.4 Contraintes: lignes HTA existante, réseau:"
            anchor_name = "site_group/contr_reglem_001"
        elif key.startswith('site_group/c') and len(key) == 14:
            label = "1.6 commentaire"
            anchor_name = "site_group/commentaire"

    elif key.startswith("batiment_group"):
        section_name = "Batiment Group"
        anchor_name = "batiment_group"
        if key == "batiment_group/info_bati":
            label = "2.1 Information sur les bâtiments: Âge, plans/DOE à disposition"
            anchor_name = "batiment_group/info_bati"
        elif key.startswith("batiment_group/c") and len(key) == 18:
            label = "2.3 Commentaire sur les vues pignon et long pan"
            anchor_name = "batiment_group/commentaire_pignon"
        elif key == "batiment_group/d_pign_lpan":
            label = "2.4 Dimensions pignons et long pan"
            anchor_name = "batiment_group/dimensions_pignons"
        elif key == "batiment_group/hbp_hf":
            label = "2.5 Hauteur bas de pente, hauteur faitage (mesure)"
            anchor_name = "batiment_group/hauteur_pente"
        elif key == "batiment_group/t_secu_EPI":
            label = "2.6 Type de sécurisation (EPI) échafaudage, garde-corps, etc."
            anchor_name = "batiment_group/securisation"
        elif key == "batiment_group/T_charpente":
            label = "2.9 Type de charpente"
            anchor_name = "batiment_group/type_charpente"
        elif key == "batiment_group/P_charpente":
            label = "2.10 Type de pannes, dimensions des pannes et dimensions(s) des entraxes"
            anchor_name = "batiment_group/type_pannes"
        elif key == "batiment_group/M_couver":
            label = "2.13 Matériau, isolation de la couverture"
            anchor_name = "batiment_group/materiau_couverture"
        elif key == "batiment_group/R_couver":
            label = "2.16 Référence du matériau de couverture (marque, modèle)"
            anchor_name = "batiment_group/reference_couverture"
        elif key == "batiment_group/d_couver":
            label = "2.17 Dimension du matériau de couverture, si applicable - important"
            anchor_name = "batiment_group/dimension_couverture"
        elif key == "batiment_group/c_inter":
            label = "2.19 Commentaire sur les intérieurs du bâtiment"
            anchor_name = "batiment_group/commentaire_interieurs"
        elif key == "batiment_group/renov_gener":
            label = "2.21 Rénovation: Observations générales : corrosion, humidité, étanchéité, etc."
            anchor_name = "batiment_group/renovation_observations"
        elif key == "batiment_group/renov_attendus":
            label = "2.22 Préciser les travaux attendus pour la rénovation (désamiantage, désenfumage, translucide, etc.)"
            anchor_name = "batiment_group/travaux_renovation"

    elif key.startswith("electricite_group"):
        section_name = "Electricite Group"
        anchor_name = "electricite_group"
        if key == "electricite_group/t_ombra":
            label = "3.1 Masque proche (ombrage): position et dimension (approx.) des obstacles"
            anchor_name = "electricite_group/masque_proche"
        elif key == "electricite_group/s91":
            label = "3.2 Masque proche (ombrage): photo/vidéo de l'environnement proche"
            anchor_name = "electricite_group/s91"
        elif key == "electricite_group/racc_indi":
            label = "3.10 ACI / raccordement indirect ?"
            anchor_name = "electricite_group/raccordement_indirect"
        elif key.startswith("electricite_group/c") and (len(key) == 22 or len(key) == 21):
            label = "3.3 Commentaire sur le masque proche"
            anchor_name = "electricite_group/commentaire_masque"
        elif key.startswith("electricite_group/s") and (len(key) == 22 or len(key) == 21):
            label = "3.4 Masque proche (ombrage): vidéo de l'environnement proche"
            anchor_name = "electricite_group/video_masque"
        elif key == "electricite_group/pass_dc":
            label = "3.5 Passage DC, descentes de chemin de câbles"
            anchor_name = "electricite_group/passage_dc"
        elif key == "electricite_group/pass_AC":
            label = "3.9 Passage des câbles AC jusqu'au TGBT (ACI) ou PDL à créer (VT), nature des revêtements à traverser"
            anchor_name = "electricite_group/passage_ac"
        elif key == "electricite_group/cat_compteur":
            label = "3.13 Catégorie du compteur existant (C1 à C5), puissance de raccordement actuelle"
            anchor_name = "electricite_group/categorie_compteur"
        elif key == "electricite_group/dim_arr_elec":
            label = "3.14 Dimensionnement de l'arrivée électricité existante (matériau, section)"
            anchor_name = "electricite_group/dimension_arrivee"
        elif key == "electricite_group/s131":
            label = "3.15 Transformateur existant (public, privé): photo"
            anchor_name = "electricite_group/transformateur_photo"

    elif key.startswith("info_compl"):
        section_name = "Informations Complémentaires"
        anchor_name = "info_compl"
        if key.startswith("info_compl/c") and len(key) == 15:
            label = "4.2 Commentaire sur le contrat d'électricité"
            anchor_name = "info_compl/commentaire_contrat"
        elif key.startswith("info_compl/s") and len(key) == 15:
            label = "4.3 Facture électrique (pour le calcul des taxes)"
            anchor_name = "info_compl/facture_electrique"

    else:
        label = key

    section_html = f'<h2 id="{anchor_name}">{section_name}</h2>' if section_name else ""
    return f'{section_html}<p><div class="label">{label}:</div> <div class="value">{value}</div></p><br>' \
        if (key != "_attachments" and key != "_geolocation" and (not (key.startswith("batiment_group/s") and len(key) == 18)) \
            and (not (key.startswith("site_group/s") and len(key) == 14)) \
            and (not (key.startswith("electricite_group/s") and (len(key) == 22 or len(key) == 21))) \
            and (not (key.startswith("info_compl/s") and len(key) == 15))) else ""

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
