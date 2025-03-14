import argparse
from core.summarizer import Summarizer

def main():
    parser = argparse.ArgumentParser(description="Summarize medical text files with LLM")
    parser.add_argument("input_path", help="path to a text file or directory of text files corresponding to singular patient")
    parser.add_argument("--output_path", default=None, help="path to write the summaries to")
    parser.add_argument("--model", default="gpt-4o-mini", help="the model to use for summarization")
    args = parser.parse_args()

    summarizer = Summarizer(args.model)
    sum = summarizer.process(args.input_path, args.output_path)
    print(sum)

if __name__ == "__main__":
    main()