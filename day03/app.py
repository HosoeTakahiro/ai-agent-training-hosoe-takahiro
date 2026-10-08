from __future__ import annotations

import argparse
import json
import logging
import sys

import boto3

from typing import Any, Dict, List

def build_parser() -> argparse.ArgumentParser:
    """Day03のCLI引数を定義します（要件文とリトライ回数）。"""
    p = argparse.ArgumentParser(prog="day03")
    p.add_argument("--requirements", required=True)
    p.add_argument("--max-retry", type=int, default=1)
    return p

def _validate_args(args: argparse.Namespace) -> None:
    """引数の簡易バリデーションを行います（入力不備は exit code=2）。"""
    if not args.requirements:
        raise ValueError("--requirements is required")
    if not (0 <= args.max_retry <= 3):
        raise ValueError("--max-retry must be between 0 and 3")

def call_llm(prompt: str) -> str:
    session = boto3.Session(profile_name="default")
    client = session.client("bedrock-runtime", region_name="ap-northeast-1")

    body = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1024,
        "temperature": 0
    }

    response = client.invoke_model(
        modelId="nvidia.nemotron-nano-12b-v2",  # ← ここは使うモデルに合わせて
        body=json.dumps(body),
        accept="application/json",
        contentType="application/json",
    )

    payload = json.loads(response["body"].read())

    return payload["choices"][0]["message"]["content"]

def generate_json(requirements: str) -> str:
    """要件文字列から、JSON文字列（本文のみ）を生成して返します。

    この関数を実装すると、`python -m day03.app --requirements ...` が動くようになります。

    実装ガイド：
    - LLMに「JSONだけを返す」ように強く指示する
    - `title` / `tasks` / `risks` を必ず含める
    - `tasks` は配列で、各要素に `id` / `description` / `acceptance_criteria` を含める
    - 返す文字列は JSON として `json.loads()` できる必要がある

    注意：
    - 余計な前置き/後置きの文章を混ぜない
    - 壊れやすいので、プロンプトは短く・形式を固定する
    """

    """
    LLM を使って JSON を生成する。
    壊れた JSON が返る可能性があるので、main() 側でリトライする。
    """
    prompt = (
        "You must output ONLY valid JSON. No explanation, no commentary, no code block.\n"
        "Output format:\n"
        "{\n"
        "  \"title\": \"依頼の要約タイトル\",\n"
        "  \"tasks\": [\n"
        "    {\n"
        "      \"id\": 1,\n"
        "      \"description\": \"作業内容\",\n"
        "      \"acceptance_criteria\": \"完了条件\"\n"
        "    }\n"
        "  ],\n"
        "  \"risks\": [\"想定リスク\"]\n"
        "}\n"
        "Rules:\n"
        "- Output JSON only.\n"
        "- Do not include any text before or after the JSON.\n"
        "- All keys must exist: title, tasks, risks.\n"
        "- tasks must be a list of objects with id, description, acceptance_criteria.\n"
        "- The JSON must be parseable by json.loads().\n"
        f"Requirements: {requirements}"
    )

    response = call_llm(prompt)

    if response is None:
        raise ValueError("LLM returned None")

    if isinstance(response, str) and response.strip() == "":
        raise ValueError("LLM returned empty string")

    data = json.loads(response)

    return json.dumps(data, ensure_ascii=False, indent=2)


def validate_json(text: str) -> Dict[str, Any]:
    """生成結果のJSONを検証します（必須キーと型）。"""
    obj = json.loads(text)
    for key in ("title", "tasks", "risks"):
        if key not in obj:
            raise ValueError(f"missing key: {key}")
    if not isinstance(obj.get("tasks"), list):
        raise ValueError("tasks must be a list")
    return obj

def main(argv: List[str] | None = None) -> int:
    """CLIのエントリポイントです。

    JSON生成→検証→（失敗時は再生成）までを制御します。受講者は `generate_json()` を実装します。
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        _validate_args(args)
    except Exception as e:
        logging.error(str(e))
        print(str(e), file=sys.stderr)
        return 2

    last_err: Exception | None = None
    for _ in range(args.max_retry + 1):
        try:
            text = generate_json(args.requirements)
            # if not text or text.strip() == "":
            #     raise ValueError("LLM returned empty output")
            validate_json(text)
            print(text)
            return 0
        except NotImplementedError as e:
            logging.error(str(e))
            print(str(e), file=sys.stderr)
            return 1
        except Exception as e:
            last_err = e

    msg = str(last_err) if last_err else "validation failed"
    logging.error(msg)
    print(msg, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
