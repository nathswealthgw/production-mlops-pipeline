import argparse
import asyncio
import statistics
import time

import httpx


async def execute(url: str, concurrency: int, requests: int) -> tuple[float, float]:
    payload = {
        "age": 35,
        "monthly_income": 8200,
        "credit_score": 700,
        "loan_amount": 180000,
        "loan_term_months": 240,
    }

    async def one(client: httpx.AsyncClient) -> float:
        started = time.perf_counter()
        response = await client.post(url, json=payload, headers={"x-signature": "invalid"})
        _ = response.status_code
        return (time.perf_counter() - started) * 1000

    latencies = []
    async with httpx.AsyncClient(timeout=5) as client:
        semaphore = asyncio.Semaphore(concurrency)

        async def guarded() -> None:
            async with semaphore:
                latencies.append(await one(client))

        await asyncio.gather(*[guarded() for _ in range(requests)])

    return statistics.mean(latencies), max(latencies)


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple async load harness")
    parser.add_argument("--url", default="http://localhost:8000/api/v1/predictions")
    parser.add_argument("--concurrency", type=int, default=20)
    parser.add_argument("--requests", type=int, default=200)
    args = parser.parse_args()

    avg, p99 = asyncio.run(execute(args.url, args.concurrency, args.requests))
    print(f"mean_latency_ms={avg:.2f} p99_like_ms={p99:.2f}")


if __name__ == "__main__":
    main()
