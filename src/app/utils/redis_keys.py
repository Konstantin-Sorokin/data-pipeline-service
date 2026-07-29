class CacheKey:
    @staticmethod
    def file_sync(candidate_id: str) -> str:
        return f"files_sync:{candidate_id}"
