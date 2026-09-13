"use client";

import { useState } from "react";

interface Repository {
  id: string;
  repo_url: string;
  owner: string;
  name: string;
  branch: string | null;
  status: string;
  file_count: number;
  chunk_count: number;
  error_message: string | null;
}

interface Source {
  file_path: string;
  language: string;
  start_line: number;
  end_line: number;
  distance: number;
}

interface AskResponse {
  answer: string;
  sources: Source[];
}

export default function Home() {
  const [repoUrl, setRepoUrl] = useState("");
  const [repository, setRepository] = useState<Repository | null>(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<AskResponse | null>(null);

  const [loadingRepository, setLoadingRepository] = useState(false);
  const [loadingQuestion, setLoadingQuestion] = useState(false);
  const [error, setError] = useState("");

  const API_URL =
    process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

  async function addRepository() {
    if (!repoUrl.trim()) {
      setError("Please enter a GitHub repository URL.");
      return;
    }

    setLoadingRepository(true);
    setError("");
    setRepository(null);
    setAnswer(null);

    try {
      const response = await fetch(
        `${API_URL}/api/repositories`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            repo_url: repoUrl,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to process repository."
        );
      }

      setRepository(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong."
      );
    } finally {
      setLoadingRepository(false);
    }
  }

  async function askQuestion() {
    if (!repository) {
      setError("Please add a repository first.");
      return;
    }

    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    setLoadingQuestion(true);
    setError("");
    setAnswer(null);

    try {
      const response = await fetch(
        `${API_URL}/api/repositories/${repository.id}/ask`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: question,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to answer question."
        );
      }

      setAnswer(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong."
      );
    } finally {
      setLoadingQuestion(false);
    }
  }

  return (
    <main className="min-h-screen bg-zinc-950 text-white">
      <div className="mx-auto max-w-5xl px-6 py-12">

        {/* Header */}
        <div className="mb-10 text-center">
          <h1 className="text-4xl font-bold tracking-tight">
            RepoRAG
          </h1>

          <p className="mt-3 text-zinc-400">
            AI-powered GitHub Repository Assistant
          </p>
        </div>

        {/* Repository Section */}
        <section className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
          <h2 className="text-xl font-semibold">
            Add Repository
          </h2>

          <p className="mt-2 text-sm text-zinc-400">
            Enter a public GitHub repository URL to analyze its codebase.
          </p>

          <div className="mt-5 flex flex-col gap-3 sm:flex-row">
            <input
              type="text"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              placeholder="https://github.com/owner/repository"
              className="flex-1 rounded-xl border border-zinc-700 bg-zinc-950 px-4 py-3 text-white outline-none placeholder:text-zinc-500 focus:border-zinc-500"
            />

            <button
              onClick={addRepository}
              disabled={loadingRepository}
              className="rounded-xl bg-white px-6 py-3 font-medium text-black transition hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loadingRepository
                ? "Processing..."
                : "Add Repository"}
            </button>
          </div>

          {/* Error */}
          {error && (
            <div className="mt-4 rounded-xl border border-red-900 bg-red-950/40 p-4 text-sm text-red-300">
              {error}
            </div>
          )}
        </section>

        {/* Repository Information */}
        {repository && (
          <section className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-xl font-semibold">
                  {repository.owner}/{repository.name}
                </h2>

                <p className="mt-1 text-sm text-zinc-400">
                  {repository.repo_url}
                </p>
              </div>

              <span className="w-fit rounded-full bg-zinc-800 px-4 py-2 text-sm">
                {repository.status}
              </span>
            </div>

            <div className="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-3">
              <div className="rounded-xl bg-zinc-950 p-4">
                <p className="text-sm text-zinc-500">
                  Files
                </p>
                <p className="mt-1 text-2xl font-semibold">
                  {repository.file_count}
                </p>
              </div>

              <div className="rounded-xl bg-zinc-950 p-4">
                <p className="text-sm text-zinc-500">
                  Chunks
                </p>
                <p className="mt-1 text-2xl font-semibold">
                  {repository.chunk_count}
                </p>
              </div>

              <div className="rounded-xl bg-zinc-950 p-4">
                <p className="text-sm text-zinc-500">
                  Branch
                </p>
                <p className="mt-1 text-2xl font-semibold">
                  {repository.branch || "N/A"}
                </p>
              </div>
            </div>
          </section>
        )}

        {/* Ask Question */}
        {repository && (
          <section className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
            <h2 className="text-xl font-semibold">
              Ask About the Repository
            </h2>

            <p className="mt-2 text-sm text-zinc-400">
              Ask a question about the codebase.
            </p>

            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="How does the authentication system work?"
              rows={4}
              className="mt-5 w-full resize-none rounded-xl border border-zinc-700 bg-zinc-950 px-4 py-3 text-white outline-none placeholder:text-zinc-500 focus:border-zinc-500"
            />

            <button
              onClick={askQuestion}
              disabled={loadingQuestion}
              className="mt-4 rounded-xl bg-white px-6 py-3 font-medium text-black transition hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loadingQuestion
                ? "Thinking..."
                : "Ask Question"}
            </button>
          </section>
        )}

        {/* Answer */}
        {answer && (
          <section className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
            <h2 className="text-xl font-semibold">
              Answer
            </h2>

            <div className="mt-4 whitespace-pre-wrap rounded-xl bg-zinc-950 p-5 leading-7 text-zinc-200">
              {answer.answer}
            </div>

            {/* Sources */}
            {answer.sources.length > 0 && (
              <div className="mt-6">
                <h3 className="font-semibold">
                  Sources
                </h3>

                <div className="mt-3 space-y-3">
                  {answer.sources.map((source, index) => (
                    <div
                      key={index}
                      className="rounded-xl border border-zinc-800 bg-zinc-950 p-4"
                    >
                      <p className="font-mono text-sm text-white">
                        {source.file_path}
                      </p>

                      <p className="mt-1 text-sm text-zinc-500">
                        {source.language} · lines{" "}
                        {source.start_line}-
                        {source.end_line}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </section>
        )}
      </div>
    </main>
  );
}