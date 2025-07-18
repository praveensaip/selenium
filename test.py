import requests
import uuid
from faker import Faker
import random, string

faker = Faker()
for i in range(10):
    token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1MWU4NmRjMmM4Nzg2YjNjMjgzN2QyNCIsImZpcnN0TmFtZSI6IlByYXZlZW5rdW1hciIsImxhc3ROYW1lIjoiUyIsImVtYWlsIjoicHJhdmVlbnNhaXA5OUBnbWFpbC5jb20iLCJvcmdhbml6YXRpb24iOiJBTkIgU3lzdGVtcyIsInRlbmFudCI6IkluaG91c2VfUmVwb3J0Iiwicm9sZXMiOlsiU3VwZXJ1c2VyIiwiRGVtbyJdLCJsb2dpbiI6InByYXZlZW5fSW5ob3VzZSIsInByb2R1Y3QiOiJlVHJhY2tQbHVzIiwiZGVmYXVsdFJvbGUiOiJTdXBlcnVzZXIiLCJoYXNSZXBvcnRBY2Nlc3MiOmZhbHNlLCJzb3VyY2UiOiJ1aSIsImVudmlyb25tZW50Ijoic3RhZ2UiLCJncm91cCI6InFhX3Rlc3QiLCJhcHBseUdldEFjbCI6dHJ1ZSwiaWF0IjoxNzUyNDk1NTgzLCJleHAiOjE3NTI0OTk3ODN9.Mw9EzqrNqRUp8oD5pbJz2-1uKwviX9-5xRe-Ev80maY"
    url = "https://api-plus-stage.anbetrack.com/core/api/v1/command"
    auth = {
        "Content-Type":"application/json",
        "Authorization": token
    }
    idd = lambda : str(uuid.uuid4())
    name = lambda : faker.first_name()
    num = lambda : random.choices(range(1,10000))[0]

    print(name(),num(),idd())

    pay = {
        "application": "eTrackPlus",
        "model": "eeProjectsinhouse",
        "product": "eTrackPlus",
        "type": "create",
        "isAsync": False,
        "isForce": False,
        "skipSave": False,
        "payload": {
            "id": idd(),
            "eeName": name(),
            "accountNumber": num(),
            "address": name(),
            "calculatedKw": num(),
            "_context": {
                "id": "bde0e132-87f1-4ecc-8247-95a18bfe5222",
                "entityType": "model",
                "entity": "programsTest",
                "instance": "Direct Install",
                "code": "DI-001"
            }
        }
    }
    req = requests.post(url,headers=auth, json=pay)
    print(req.status_code)
    de = req.json()
    idss = de['insertedId']
    ops_id = de['ops'][0]["id"]
    cmd_url = "https://api-plus-stage.anbetrack.com/core/api/v1/comments"

    comm_payload = {
        "application": "eTrackPlus",
        "model": "eeProjectsinhouse",
        "product": "eTrackPlus",
        "type": "submitWorkflow",
        "isAsync": False,
        "isForce": False,
        "isValidate": False,
        "skipSave": True,
        "payload": {
            "id": ops_id,
            "accountNumber": num(),
            "calculatedKw": num(),
            "_context": {
                "id": "bde0e132-87f1-4ecc-8247-95a18bfe5222",
                "entityType": "model",
                "entity": "programsTest",
                "instance": "Direct Install",
                "code": "DI-001"
            },
            "_source": "platform",
            "_channel": "platform",
            "_isDeleted": False,
            "createdBy": "praveen_Inhouse",
            "updatedBy": "praveen_Inhouse",
            "updatedAt": "2025-07-14T11:42:05.333Z",
            "_workflow": {
                "processModelId": "67ac91947af92ccd184cff8c",
                "processInstanceId": "6874ed0101f050d98993e3bb",
                "inboxItemId": "6874ed0201f050d98993e3bd",
                "inboxItem": {
                    "_id": "6874ed0201f050d98993e3bd",
                    "assignedBy": "praveen_Inhouse",
                    "assignedTo": [
                        "Superuser"
                    ],
                    "currentOwner": "Superuser",
                    "status": "assigned",
                    "createdAt": "2025-07-14T11:41:54.267Z"
                },
                "currentState": {
                    "id": "Task_0fvlqyq",
                    "name": "Created",
                    "subType": "USER_TASK"
                },
                "processInstanceDate": "2025-07-14T11:41:53.177Z",
                "currentTaskDate": "2025-07-14T11:41:54.233Z",
                "isError": False,
                "event": "transition",
                "isRunning": False,
                "hasCommentPost": False,
                "targetState": {
                    "name": "Draft"
                }
            }
        },
        "workflow": {
            "processModelId": "67ac91947af92ccd184cff8c",
            "processInstanceId": "6874ed0101f050d98993e3bb",
            "targetId": "Task_0fvlqyq",
            "event": "update",
            "tenantId": "Inhouse_Report",
            "context": {
                "eeProjectsinhouse": {
                    "id": ops_id
                },
                "inboxItemId": "6874ed0201f050d98993e3bd",
                "wfNextTasks": [
                    "Draft"
                ],
                "tenantId": "Inhouse_Report"
            }
        },
        "comment": {
            "comment": f"<p>Workflow Status is moved from Drafy status successfully - {name()}</p>\n (Workflow status moved from Created  to Draft)",
            "accessType": "public",
            "type": "workflow",
            "context": {
                "model": "eeProjectsinhouse",
                "instanceId": ops_id
            },
            "user": {
                "login": "praveen_Inhouse",
                "role": "Superuser",
                "name": "Praveenkumar S"
            }
        },
        "criteria": {
            "_id": idss
        }
    }

    yes_payload = {
    "application": "eTrackPlus",
    "model": "eeProjectsinhouse",
    "product": "eTrackPlus",
    "type": "submitWorkflow",
    "isAsync": False,
    "isForce": False,
    "isValidate": False,
    "skipSave": True,
    "payload": {
        "id": ops_id,
        "eeName": name(),
        "accountNumber": num(),
        "address": name(),
        "calculatedKw": num(),
        "_context": {
            "id": "bde0e132-87f1-4ecc-8247-95a18bfe5222",
            "entityType": "model",
            "entity": "programsTest",
            "instance": "Direct Install",
            "code": "DI-001"
        },
        "_source": "platform",
        "_channel": "platform",
        "_isDeleted": False,
        "createdBy": "praveen_Inhouse",
        "updatedBy": "praveen_Inhouse",
        "updatedAt": "2025-07-14T12:35:45.036Z",
        "_workflow": {
            "processModelId": "67ac91947af92ccd184cff8c",
            "processInstanceId": "6874f91439f9aaed0f8197c5",
            "inboxItemId": "6874f91539f9aaed0f8197c7",
            "inboxItem": {
                "_id": "6874f91539f9aaed0f8197c7",
                "assignedBy": "praveen_Inhouse",
                "assignedTo": [
                    "Superuser"
                ],
                "currentOwner": "Superuser",
                "status": "assigned",
                "createdAt": "2025-07-14T12:33:25.359Z"
            },
            "currentState": {
                "id": "Task_0fvlqyq",
                "name": "Created",
                "subType": "USER_TASK"
            },
            "processInstanceDate": "2025-07-14T12:33:24.898Z",
            "currentTaskDate": "2025-07-14T12:33:25.277Z",
            "isError": False,
            "event": "transition",
            "isRunning": False,
            "hasCommentPost": False,
            "targetState": {
                "name": "Draft"
            }
        }
    },
    "workflow": {
        "processModelId": "67ac91947af92ccd184cff8c",
        "processInstanceId": "6874f91439f9aaed0f8197c5",
        "targetId": "Task_0fvlqyq",
        "event": "update",
        "tenantId": "Inhouse_Report",
        "context": {
            "eeProjectsinhouse": {
                "id": ops_id
            },
            "inboxItemId": "6874f91539f9aaed0f8197c7",
            "wfNextTasks": [
                "Draft"
            ],
            "tenantId": "Inhouse_Report"
        }
    },
    "comment": {
        "comment": f"<p>Status is moved to Yes - {name()}</p>\n (Workflow status moved from Created  to Draft)",
        "accessType": "public",
        "type": "workflow",
        "context": {
            "model": "eeProjectsinhouse",
            "instanceId": ops_id,
            "nameAttributeValue": "Heidi"
        },
        "user": {
            "login": "praveen_Inhouse",
            "role": "Superuser",
            "name": "Praveenkumar S"
        }
    },
    "criteria": {
        "_id": idss
    }
}

    req = requests.post(url,headers=auth, json=comm_payload)
    print(req.status_code)
    req = requests.post(url,headers=auth, json=comm_payload)
    print(req.status_code)
    req = requests.post(url,headers=auth, json=comm_payload)
    print(req.status_code)

    req = requests.post(url,headers=auth, json=yes_payload)
    print(req.status_code)
    req = requests.post(url,headers=auth, json=yes_payload)
    print(req.status_code)
    req = requests.post(url,headers=auth, json=yes_payload)
    print(req.status_code)

    public = {
        "comment": f"<p>Public Comment - {name()}</p>\n",
        "accessType": "public",
        "type": "general",
        "context": {
            "model": "eeProjectsinhouse",
            "instanceId": ops_id
        },
        "user": {
            "login": "praveen_Inhouse",
            "role": "Superuser",
            "name": "Praveenkumar S"
        }
    }
    # print("publiccc", public)
    req = requests.post(cmd_url,headers=auth, json=public)
    print(req.status_code)
    req = requests.post(cmd_url,headers=auth, json=public)
    print(req.status_code)
    req = requests.post(cmd_url,headers=auth, json=public)
    print(req.status_code)

    private = {
        "comment": f"<p>Private Command - {name()}</p>\n",
        "accessType": "private",
        "type": "general",
        "context": {
            "model": "eeProjectsinhouse",
            "instanceId": ops_id
        },
        "user": {
            "login": "praveen_Inhouse",
            "role": "Superuser",
            "name": "Praveenkumar S"
        }
    }

    req = requests.post(cmd_url,headers=auth, json=private)
    print(req.status_code)
    req = requests.post(cmd_url,headers=auth, json=private)
    print(req.status_code)
    req = requests.post(cmd_url,headers=auth, json=private)
    print(req.status_code)

    organization = {
        "comment": f"<p>Organization - {name()}</p>\n",
        "accessType": "myOrganization",
        "type": "general",
        "context": {
            "model": "eeProjectsinhouse",
            "instanceId": ops_id
        },
        "orgName": "ANB Systems",
        "user": {
            "login": "praveen_Inhouse",
            "role": "Superuser",
            "name": "Praveenkumar S"
        }
    }
    req = requests.post(cmd_url,headers=auth, json=organization)
    print(req.status_code)
    req = requests.post(cmd_url,headers=auth, json=organization)
    print(req.status_code)
    req = requests.post(cmd_url,headers=auth, json=organization)
    print(req.status_code)
    break