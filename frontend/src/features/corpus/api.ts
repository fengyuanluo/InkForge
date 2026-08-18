import { apiClient } from "@/lib/api-client";

import type {
  CorpusDocument,
  CorpusImportResult,
  CorpusJob,
  CorpusLibrary,
  CorpusSearchHit,
  CorpusUnit,
  CorpusUnitBrief,
} from "./types";

type JsonObject = Record<string, unknown>;

function transformLibrary(raw: JsonObject): CorpusLibrary {
  return {
    id: raw.id as string,
    name: raw.name as string,
    description: (raw.description as string | null) ?? null,
    tags: (raw.tags as string[]) ?? [],
    documentCount: Number(raw.document_count ?? 0),
    charCount: Number(raw.char_count ?? 0),
    createdAt: raw.created_at as string,
    updatedAt: raw.updated_at as string,
  };
}

function transformDocument(raw: JsonObject): CorpusDocument {
  return {
    id: raw.id as string,
    kind: raw.kind as string,
    title: raw.title as string,
    author: (raw.author as string | null) ?? null,
    dynasty: (raw.dynasty as string | null) ?? null,
    tags: (raw.tags as string[]) ?? [],
    metadata: (raw.metadata as Record<string, unknown>) ?? {},
    libraryIds: (raw.library_ids as string[]) ?? [],
    sourceAliases: (raw.source_aliases as string[]) ?? [],
    unitCount: Number(raw.unit_count ?? 0),
    charCount: Number(raw.char_count ?? 0),
    indexStatus: (raw.index_status as string) ?? "not_indexed",
    indexChunkCount: Number(raw.index_chunk_count ?? 0),
    indexJobId: (raw.index_job_id as string | null) ?? null,
    indexError: (raw.index_error as string | null) ?? null,
    indexedAt: (raw.indexed_at as string | null) ?? null,
    createdAt: raw.created_at as string,
    updatedAt: raw.updated_at as string,
  };
}

function transformUnit(raw: JsonObject): CorpusUnitBrief {
  return {
    id: raw.id as string,
    documentId: raw.document_id as string,
    kind: raw.kind as string,
    order: Number(raw.order ?? 0),
    title: (raw.title as string | null) ?? null,
    volume: (raw.volume as string | null) ?? null,
    charCount: Number(raw.char_count ?? 0),
    metadata: (raw.metadata as Record<string, unknown>) ?? {},
  };
}

function transformJob(raw: JsonObject): CorpusJob {
  return {
    id: raw.id as string,
    status: raw.status as string,
    progress: (raw.progress as Record<string, unknown>) ?? {},
    result: (raw.result as Record<string, unknown>) ?? {},
    error: (raw.error as Record<string, unknown>) ?? {},
    attemptCount: Number(raw.attempt_count ?? 0),
    createdAt: raw.created_at as string,
    updatedAt: raw.updated_at as string,
    startedAt: (raw.started_at as string | null) ?? null,
    finishedAt: (raw.finished_at as string | null) ?? null,
  };
}

export async function fetchCorpusLibraries(): Promise<CorpusLibrary[]> {
  const response = await apiClient.get<{ items: JsonObject[] }>("/corpus/libraries");
  return response.data.items.map(transformLibrary);
}

export async function createCorpusLibrary(data: {
  name: string;
  description?: string;
  tags?: string[];
}): Promise<CorpusLibrary> {
  const response = await apiClient.post<JsonObject>("/corpus/libraries", data);
  return transformLibrary(response.data);
}

export async function updateCorpusLibrary(
  libraryId: string,
  data: { name?: string; description?: string; tags?: string[] },
): Promise<CorpusLibrary> {
  const response = await apiClient.patch<JsonObject>(`/corpus/libraries/${libraryId}`, data);
  return transformLibrary(response.data);
}

export async function deleteCorpusLibrary(libraryId: string): Promise<void> {
  await apiClient.delete(`/corpus/libraries/${libraryId}`);
}

export async function fetchCorpusDocuments(libraryId: string): Promise<CorpusDocument[]> {
  const response = await apiClient.get<{ items: JsonObject[] }>(
    `/corpus/libraries/${libraryId}/documents`,
  );
  return response.data.items.map(transformDocument);
}

export async function updateCorpusDocument(
  documentId: string,
  data: {
    title?: string;
    author?: string;
    dynasty?: string;
    tags?: string[];
    metadata?: Record<string, unknown>;
  },
): Promise<CorpusDocument> {
  const response = await apiClient.patch<JsonObject>(`/corpus/documents/${documentId}`, data);
  return transformDocument(response.data);
}

export async function fetchCorpusUnits(documentId: string): Promise<CorpusUnitBrief[]> {
  const response = await apiClient.get<{ items: JsonObject[] }>(
    `/corpus/documents/${documentId}/units`,
  );
  return response.data.items.map(transformUnit);
}

export async function fetchCorpusUnit(unitId: string): Promise<CorpusUnit> {
  const response = await apiClient.get<JsonObject>(`/corpus/units/${unitId}`);
  return {
    ...transformUnit(response.data),
    documentTitle: response.data.document_title as string,
    author: (response.data.author as string | null) ?? null,
    dynasty: (response.data.dynasty as string | null) ?? null,
    text: response.data.text as string,
  };
}

function transformImport(raw: JsonObject): CorpusImportResult {
  return {
    libraryId: raw.library_id as string,
    documentIds: (raw.document_ids as string[]) ?? [],
    importedCount: Number(raw.imported_count ?? 0),
    deduplicatedCount: Number(raw.deduplicated_count ?? 0),
    unitCount: Number(raw.unit_count ?? 0),
    jobId: raw.job_id as string,
  };
}

export async function uploadCorpus(file: File, libraryId?: string): Promise<CorpusImportResult> {
  const form = new FormData();
  form.append("file", file);
  if (libraryId) form.append("library_id", libraryId);
  const response = await apiClient.post<JsonObject>("/corpus/imports/upload", form, {
    headers: { "Content-Type": "multipart/form-data" },
    timeout: 0,
  });
  return transformImport(response.data);
}

export async function importCorpusFromRoot(
  path: string,
  libraryId?: string,
): Promise<CorpusImportResult> {
  const response = await apiClient.post<JsonObject>(
    "/corpus/imports/from-root",
    { path, library_id: libraryId || null },
    { timeout: 0 },
  );
  return transformImport(response.data);
}

export async function fetchProjectCorpusLibraries(projectId: string): Promise<string[]> {
  const response = await apiClient.get<{ library_ids: string[] }>(
    `/corpus/projects/${projectId}/libraries`,
  );
  return response.data.library_ids ?? [];
}

export async function updateProjectCorpusLibraries(
  projectId: string,
  libraryIds: string[],
): Promise<string[]> {
  const response = await apiClient.put<{ library_ids: string[] }>(
    `/corpus/projects/${projectId}/libraries`,
    { library_ids: libraryIds },
  );
  return response.data.library_ids ?? [];
}

export async function searchCorpus(data: {
  query: string;
  projectId?: string;
  libraryIds?: string[];
}): Promise<CorpusSearchHit[]> {
  const response = await apiClient.post<{ items: JsonObject[] }>("/corpus/search", {
    query: data.query,
    project_id: data.projectId || null,
    library_ids: data.libraryIds ?? [],
    limit: 8,
  });
  return response.data.items.map((raw) => ({
    documentId: raw.document_id as string,
    unitId: raw.unit_id as string,
    chunkIndex: Number(raw.chunk_index ?? 0),
    text: raw.text as string,
    contextText: (raw.context_text as string | null) ?? null,
    score: Number(raw.score ?? 0),
    matchedBy: raw.matched_by as string,
    title: raw.title as string,
    author: (raw.author as string | null) ?? null,
    dynasty: (raw.dynasty as string | null) ?? null,
    documentKind: raw.document_kind as string,
    unitKind: raw.unit_kind as string,
    unitTitle: (raw.unit_title as string | null) ?? null,
    volume: (raw.volume as string | null) ?? null,
    unitOrder: Number(raw.unit_order ?? 0),
    tags: (raw.tags as string[]) ?? [],
    libraryIds: (raw.library_ids as string[]) ?? [],
  }));
}

export async function rebuildCorpus(): Promise<{ documentCount: number; jobId: string }> {
  const response = await apiClient.post<{ document_count: number; job_id: string }>(
    "/corpus/rebuild",
    undefined,
    { timeout: 0 },
  );
  return { documentCount: response.data.document_count, jobId: response.data.job_id };
}

export async function fetchCorpusJobs(): Promise<CorpusJob[]> {
  const response = await apiClient.get<{ items: JsonObject[] }>("/corpus/jobs");
  return response.data.items.map(transformJob);
}

export async function controlCorpusJob(
  jobId: string,
  action: "pause" | "resume" | "cancel" | "retry",
): Promise<CorpusJob> {
  const response = await apiClient.post<JsonObject>(`/corpus/jobs/${jobId}/${action}`);
  return transformJob(response.data);
}
