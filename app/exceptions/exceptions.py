class ImageUploadFailed(Exception):
    def __init__(self, message="An error occurred uploading your image"):
        self.message = message
        super().__init__(self.message)


class ExerciseUploadFailed(Exception):
    def __init__(self, message="An error occurred uploading your exercise to our database"):
        self.message = message
        super().__init__(self.message)
