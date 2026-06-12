from backend.modules.memory.ingestion.content_analyzer import ContentAnalyzer


class DecisionEngine:

    @staticmethod
    def decide(text: str, file_type: str) -> dict:
        """
        Analyzes content and makes ingestion decision.

        Returns full analysis with chunking strategy.
        """
        analysis = ContentAnalyzer.analyze(text, file_type)

        # Determine which ChromaDB collection to use
        collection = DecisionEngine._get_collection(file_type)

        analysis["collection"] = collection

        return analysis

    @staticmethod
    def _get_collection(file_type: str) -> str:
        """
        Maps file type to ChromaDB collection name.

        Each collection stores different types of memories.
        """

        collection_map = {
            "pdf": "knowledge_base",
            "docx": "knowledge_base",
            "txt": "knowledge_base",
            "markdown": "knowledge_base",
            "csv": "knowledge_base",
            "json": "knowledge_base",
            "code": "code_memory",
            "text_snippet": "personal_memory",
        }

        return collection_map.get(file_type, "knowledge_base")