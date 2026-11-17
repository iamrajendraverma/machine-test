import json

from rag.medical import medical_result
from rag.policy import retrieve_evidence  # noqa: F401  (policy pipeline entry point)


def main():
    query = "Show the latest HbA1c result for patient P001"
    output = medical_result(query)
    print(f" Output {json.dumps(output, indent=4)}")


if __name__ == "__main__":
    main()
