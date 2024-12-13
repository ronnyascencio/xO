import nuke
import hiero.core
import requests
import json
from datetime import datetime, timedelta

# Token de API de Notion y el ID de la base de datos
API_TOKEN = "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"
DATABASE_ID = "13aaa963-0391-806d-8926-db6931b44e4e"

# URL para crear una página en la base de datos de Notion
url = "https://api.notion.com/v1/pages"

# Encabezados para la solicitud
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


def getStatus(trackItem):
    status = 'OK'
    if not trackItem.isMediaPresent():
        status = 'OFFLINE'
    return status


def getSrcIn(trackItem):
    fps = trackItem.parent().parent().framerate()
    clip = trackItem.source()
    clipstartTimeCode = clip.timecodeStart()
    return hiero.core.Timecode.timeToString(
        int(clipstartTimeCode + trackItem.sourceIn()),
        fps,
        hiero.core.Timecode.kDisplayTimecode
    )


def getSrcOut(trackItem):
    fps = trackItem.parent().parent().framerate()
    clip = trackItem.source()
    clipstartTimeCode = clip.timecodeStart()
    return hiero.core.Timecode.timeToString(
        int(clipstartTimeCode + trackItem.sourceOut()),
        fps,
        hiero.core.Timecode.kDisplayTimecode
    )


def create_project_from_nstudio():
    try:
        project = hiero.core.projects()[-1]
        project_name = project.name()
        print(f"Creando proyecto: {project_name} en Notion...")

        # Datos del proyecto en Notion
        data = {
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Project Name": {
                    "title": [{"text": {"content": project_name}}]
                },
                "Status": {
                    "status": {"name": "Active"}
                },
                "Client": {
                    "rich_text": [{
                        "text": {
                            "content": "Cliente Nuevo"
                        }
                    }]
                },
                "Start Date": {
                    "date": {
                        "start": datetime.now().strftime("%Y-%m-%d")
                    }
                },
                "End Date": {
                    "date": {
                        "start": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
                    }
                },
                "Sequences": {
                    "relation": []
                },
                "Assets": {
                    "relation": []
                }
            }
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            project_page_id = response.json()["id"]
            print("Proyecto creado exitosamente en Notion.")
            create_sequences_from_nstudio(project, project_page_id)
        else:
            print(f"Error al crear el proyecto: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"Error: {e}")


def create_sequences_from_nstudio(project, project_page_id):
    try:
        sequence_ids = []

        # Obtener todas las secuencias del proyecto
        for sequence in project.sequences():
            print(f"Procesando secuencia: {sequence.name()}")

            # Obtener tracks de video y audio
            vTracks = sequence.videoTracks()
            aTracks = sequence.audioTracks()
            tracks = vTracks + aTracks

            for track in tracks:
                track_items = []
                for item in track:
                    if isinstance(item, hiero.core.TrackItem):
                        track_items.append({
                            "name": item.name(),
                            "status": getStatus(item),
                            "track": track.name(),
                            "source_in": getSrcIn(item),
                            "source_out": getSrcOut(item),
                            "duration": item.duration(),
                            "source_name": item.source().name(),
                            "media_type": "Video" if track in vTracks else "Audio"
                        })

                if track_items:  # Si el track tiene items
                    sequence_name = f"{sequence.name()}_{track.name()}"
                    print(f"Creando secuencia: {sequence_name} en Notion...")

                    # Crear descripción detallada de los clips
                    clips_description = "\n".join([
                        f"Clip: {item['name']} | "
                        f"Status: {item['status']} | "
                        f"Duration: {item['duration']} | "
                        f"TC: {item['source_in']} - {item['source_out']}"
                        for item in track_items
                    ])

                    sequence_data = {
                        "parent": {"database_id": DATABASE_ID},
                        "properties": {
                            "Project Name": {
                                "title": [{"text": {"content": sequence_name}}]
                            },
                            "Status": {
                                "status": {"name": "Active"}
                            },
                            "Client": {
                                "rich_text": [{
                                    "text": {
                                        "content": f"Type: {track_items[0]['media_type']}\nClips: {len(track_items)}\n{clips_description}"
                                    }
                                }]
                            },
                            "Start Date": {
                                "date": {
                                    "start": datetime.now().strftime("%Y-%m-%d")
                                }
                            }
                        }
                    }

                    sequence_response = requests.post(url, headers=headers, json=sequence_data)

                    if sequence_response.status_code == 200:
                        sequence_id = sequence_response.json()["id"]
                        sequence_ids.append({"id": sequence_id})
                        print(f"Secuencia '{sequence_name}' creada exitosamente.")
                    else:
                        print(f"Error al crear la secuencia '{sequence_name}': {sequence_response.status_code}")
                        print(sequence_response.text)

        # Actualizar el proyecto con las relaciones de las secuencias
        if sequence_ids:
            update_url = f"https://api.notion.com/v1/pages/{project_page_id}"
            update_data = {
                "properties": {
                    "Sequences": {
                        "relation": sequence_ids
                    }
                }
            }

            update_response = requests.patch(update_url, headers=headers, json=update_data)
            if update_response.status_code == 200:
                print("Relaciones de secuencias actualizadas en el proyecto.")
            else:
                print("Error al actualizar las relaciones de secuencias.")
                print(update_response.text)

    except Exception as e:
        print(f"Error al crear secuencias: {e}")


def add_notion_menu():
    menu = nuke.menu('Nuke')
    notion_menu = menu.addMenu('xO')
    notion_menu.addCommand('Project to Notion', create_project_from_nstudio)


add_notion_menu()

print("Menú 'xO' añadido con éxito.")