def coordinator_agent(sub_queries):

    categories = {
        item["category"]
        for item in sub_queries
    }

    routes = []

    if "lab" in categories:
        routes.append("lab")

    if "medication" in categories:
        routes.append("medication")

    return routes or ["response"]