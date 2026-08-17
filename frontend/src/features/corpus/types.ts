export interface CorpusLibrary {
  id: string;
  name: string;
  description: string | null;
  tags: string[];
  documentCount: number;
  charCount: number;
  createdAt: string;
  updatedAt: string;
}

export interface CorpusDocument {
  id: string;
  kind: string;
  title: string;
  author: string | null;
  dynasty: string | null;
  tags: string[];
  metadata: Record<string, unknown>;
  libraryIds: string[];
  sourceAliases: string[];
  unitCount: number;
  charCount: number;
  indexStatus: string;
  indexChunkCount: number;
  indexJobId: string | null;
  indexError: string | null;
  indexedAt: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface CorpusUnitBrief {
  id: string;
  documentId: string;
  kind: string;
  order: number;
  title: string | null;
  volume: string | null;
  charCount: number;
  metadata: Record<string, unknown>;
}

export interface CorpusUnit extends CorpusUnitBrief {
  documentTitle: string;
  author: string | null;
  dynasty: string | null;
  text: string;
}

export interface CorpusImportResult {
  libraryId: string;
  documentIds: string[];
  importedCount: number;
  deduplicatedCount: number;
  unitCount: number;
  jobId: string;
}

export interface CorpusSearchHit {
  documentId: string;
  unitId: string;
  chunkIndex: number;
  text: string;
  contextText: string | null;
  score: number;
  matchedBy: string;
  title: string;
  author: string | null;
  dynasty: string | null;
  documentKind: string;
  unitKind: string;
  unitTitle: string | null;
  volume: string | null;
  unitOrder: number;
  tags: string[];
  libraryIds: string[];
}

export interface CorpusJob {
  id: string;
  status: string;
  progress: Record<string, unknown>;
  result: Record<string, unknown>;
  error: Record<string, unknown>;
  attemptCount: number;
  createdAt: string;
  updatedAt: string;
  startedAt: string | null;
  finishedAt: string | null;
}
