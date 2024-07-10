from app.resource_mgmt import get_resource, patch_resource
from app.job_mgmt import submit_file, check_job_manager, submit_hybrid_job, check_job_info, delete_job, get_job_status, get_job_result

def display_menu():
    while True:
        print("KISTI's hybrid interface")
        print("============== Menu ==============")
        print("[1] Get resource information")
        print("[2] Update resource status (on/off)")
        print("----------------------------------")
        print("[3] Submit files to API server")
        print("[4] Check job manager")
        print("[5] Submit hybrid job")
        print("[6] Check job information")
        print("[7] Delete job")
        print("[8] Get job status")
        print("[9] Get job result")
        print("----------------------------------")
        print("[0] Exit")
        print("==================================")
        num = input("Enter the number: ")

        if num == '1':
            get_resource()
        elif num == '2':
            patch_resource()
        elif num == '3':
            submit_file()
        elif num == '4':
            check_job_manager()
        elif num == '5':
            submit_hybrid_job()
        elif num == '6':
            job_uuid = input("Enter job UUID: ")
            job_uuid = "9f82b9de-2d24-45fe-8a4e-efc8dd6175e4"
            check_job_info(job_uuid)
        elif num == '7':
            job_uuid = input("Enter job UUID: ")
            job_uuid = "9f82b9de-2d24-45fe-8a4e-efc8dd6175e4"
            delete_job(job_uuid)
        elif num == '8':
            job_uuid = input("Enter job UUID: ")
            job_uuid = "9f82b9de-2d24-45fe-8a4e-efc8dd6175e4"
            get_job_status(job_uuid)
        elif num == '9':
            job_uuid = input("Enter job UUID: ")
            job_uuid = "9f82b9de-2d24-45fe-8a4e-efc8dd6175e4"
            get_job_result(job_uuid)
        elif num == '0':
            print("Exiting the client program...")
            break
        else:
            print("Invalid choice. Please enter a number between 0 and 9.")

        print(" ")
        again = input("Would you like to execute the menu again? (y/n): ").strip().lower()
        if again != 'y':
            print("Exiting...")
            break
