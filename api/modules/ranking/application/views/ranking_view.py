from sqlalchemy.sql import text

class RankingView:
    
    def __init__(self, session):
        self.session = session
        
    def get_ranking_list(self, mes_filter = None):
        
        query_mes_filter = ""
        
        if mes_filter:
            query_mes_filter = """ WHERE "R"."month" = :mes_filter """
        
        query = """
            SELECT
                ROW_NUMBER() OVER (ORDER BY "R"."student_id" ASC) AS "ranking_position",
                "S".name AS "student_name",
                "S".last_name AS "student_last_name",
                COUNT("R"."student_id") AS "total_posts",
                AVG("R"."score") AS "average_score"
            FROM custom_ranking.ranking "R"
            LEFT JOIN custom_users."Students" "S" ON "R"."student_id" = "S"."id"
            {query_mes_filter}
            GROUP BY "R"."student_id", "S".name, "S".last_name
        """
        
        query = query.format(query_mes_filter=query_mes_filter)

        result = self.session.execute(text(query), {"mes_filter": mes_filter}).fetchall()
        ranking = []
        for row in result:
            row_dict = dict(row._mapping)
            ranking.append(row_dict)
        return ranking