class ai_camera_class():
    def __init__(self, PORT="PORT1", INDEX="INDEX1"):
        """
        define the ai camera
        PORT, the port the sensor is connected to on the novapi
        INDEX, the sensor number in the chain INDEX<1-10>
        """
        pass
    
    def ai_camera_face_learn(self, face:str, index:int):
        """
        Learn a face with a specific name and ID.
        """
        return

    def ai_camera_face_name_set(self, face1:str, face2:str, index:int):
        """
        Set the name of a learned face.
        """
        return

    def ai_camera_face_delete_all(self, index:int):
        """
        Delete all learned faces.
        """
        return

    def ai_camera_face_delete_by_id(self, face:str, index:int):
        """
        Delete a learned face by ID.
        """
        return

    def ai_camera_object_name_set(self, Item1:str, Item2:str, index:int):
        """
        Set the name of a learned object.
        """
        return

    def ai_camera_object_name_delete(self, Item:str, index:int):
        """
        Delete a learned object by ID.
        """
        return
    
    def ai_camera_speech_recognition_set_keyword(self, keyword:str, index:int):
        """
        Set the keyword for speech recognition.
        """
        return
    
    def ai_camera_image_load_model_by_id(self, model:int, index:int):
        """
        Load a custom model by ID.
        """
        return

