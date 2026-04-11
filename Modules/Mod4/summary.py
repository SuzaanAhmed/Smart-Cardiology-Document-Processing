# the code right now does not take input from the other modules, but rather takes it from within the code
# typed in the "text"

# once the previous modules are done, lemme know


from transformers import pipeline
import re

class ReportSummarizer:
    
    def __init__(self):
        print("Loading model...")
        self.summarizer = pipeline("summarization", model="t5-small")

    def generate_summary(self, text):
        input_text = "summarize: " + text

        input_len = len(text.split())
        max_len = min(60, int(input_len * 0.8))  # dynamic
        min_len = max(20, int(input_len * 0.3))

        result = self.summarizer(
            input_text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )

        summary = result[0]['summary_text'].strip()
        summary = summary[0].upper() + summary[1:]

        return summary

    def extract_key_findings(self, summary):
        sentences = re.split(r'\.\s*', summary)
        sentences = [s.strip().capitalize() for s in sentences if s.strip()]
        return sentences[:2]

    def extract_critical_points(self, text):
        critical_keywords = [
            "risk", "critical", "emergency", "severe",
            "urgent", "immediate", "attention", "complication"
        ]

        critical = []
        for sentence in text.split('.'):
            for word in critical_keywords:
                if word in sentence.lower():
                    critical.append(sentence.strip().capitalize())

        return list(set(critical))

    def process_report(self, text):
        summary = self.generate_summary(text)
        key_findings = self.extract_key_findings(summary)
        critical_points = self.extract_critical_points(text)

        return {
            "summary": summary,
            "key_findings": key_findings,
            "critical_points": critical_points
        }

if __name__ == "__main__":
    text = """
    Patient shows irregular heart rhythm with mild ST elevation.
    History of hypertension and diabetes.
    There is a high risk of cardiac complications.
    Immediate medical attention is recommended.
    """

    summarizer = ReportSummarizer()
    result = summarizer.process_report(text)

    print("\nFINAL OUTPUT:\n")
    print("\n========== REPORT SUMMARY ==========\n")

    print("Summary:")
    print(result["summary"])

    print("\nKey Findings:")
    for i, point in enumerate(result["key_findings"], 1):
        print(f"{i}. {point}")

    print("\nCritical Points:")
    if result["critical_points"]:
        for i, point in enumerate(result["critical_points"], 1):
            print(f"{i}. {point}")
    else:
        print("None")

    print("\n====================================\n")