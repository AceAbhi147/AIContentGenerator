import os


class DirectoryCreator:

    def __init__(self, resources, jobs_dir):
        self.resources = resources
        self.jobs_dir = jobs_dir

    def create_resource_directories(self, job_id):
        print("Creating the required resources directories")
        job_path = os.path.join(self.jobs_dir, job_id)
        result = {
            "job_dir": job_path
        }

        if not os.path.exists(job_path):
            os.makedirs(job_path)

        for resource in self.resources:
            resource_dir = os.path.join(job_path, resource)
            result[f'{resource}_dir'] = resource_dir
            if not os.path.exists(resource_dir):
                os.makedirs(resource_dir)
            else:
                for file in os.listdir(resource_dir):
                    file_path = os.path.join(resource_dir, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

        print("Resources Directory Created")
        return result
