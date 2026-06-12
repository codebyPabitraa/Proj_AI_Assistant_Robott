class ContentAnalyzer:

    # Word count thresholds
    SMALL_THRESHOLD = 100       # Less than 100 words = small
    MEDIUM_THRESHOLD = 500      # 100-500 words = medium
    LARGE_THRESHOLD = 3000      # 500-3000 words = large
                                # More than 3000 words = very large

    @staticmethod
    def analyze(text: str, file_type: str) -> dict:
        """
        Analyzes content and returns metadata.

        Returns:
            word_count: number of words
            size_category: small / medium / large / very_large
            file_type: original file type
            requires_chunking: True or False
            chunking_strategy: direct / semantic / hierarchical / code / csv / json / markdown
        """

        word_count = len(text.split())

        # Determine size category
        if word_count < ContentAnalyzer.SMALL_THRESHOLD:
            size_category = "small"
            requires_chunking = False

        elif word_count < ContentAnalyzer.MEDIUM_THRESHOLD:
            size_category = "medium"
            requires_chunking = False

        elif word_count < ContentAnalyzer.LARGE_THRESHOLD:
            size_category = "large"
            requires_chunking = True

        else:
            size_category = "very_large"
            requires_chunking = True

        # Determine chunking strategy based on file type
        chunking_strategy = ContentAnalyzer._get_strategy(
            file_type=file_type,
            requires_chunking=requires_chunking
        )

        return {
            "word_count": word_count,
            "size_category": size_category,
            "file_type": file_type,
            "requires_chunking": requires_chunking,
            "chunking_strategy": chunking_strategy
        }

    @staticmethod
    def _get_strategy(file_type: str, requires_chunking: bool) -> str:
        """
        Returns chunking strategy based on file type.
        """

        if not requires_chunking:
            return "direct"

        strategy_map = {
            "pdf": "semantic",
            "docx": "semantic",
            "txt": "semantic",
            "markdown": "markdown",
            "csv": "csv",
            "json": "json",
            "code": "code",
            "text_snippet": "direct"
        }

        return strategy_map.get(file_type, "semantic")
    