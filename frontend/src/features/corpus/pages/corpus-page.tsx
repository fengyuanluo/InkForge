import {
  Badge,
  Box,
  Button,
  Checkbox,
  Flex,
  Heading,
  Tabs,
  Text,
  TextArea,
  TextField,
  Tooltip,
} from "@radix-ui/themes";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import {
  BookOpen,
  FileText,
  FolderInput,
  Pause,
  Play,
  Plus,
  RefreshCw,
  RotateCcw,
  Save,
  Search,
  SlidersHorizontal,
  Trash2,
  Upload,
  X,
} from "lucide-react";
import { useEffect, useMemo, useRef, useState } from "react";
import { useTranslation } from "react-i18next";

import { ConfirmDialog, Spinner, toast } from "@/components";
import { LabeledSelect } from "@/components/select";
import { MobileAppSidebarTrigger } from "@/features/app-shell";
import { useAgentSettingsLock } from "@/features/settings/lib/agent-settings-lock";
import { fetchModels } from "@/features/settings/lib/model-api";
import { fetchSettings, updateSettings } from "@/features/settings/lib/settings-api";
import { fetchProjects } from "@/lib/api-client";

import {
  controlCorpusJob,
  createCorpusLibrary,
  deleteCorpusLibrary,
  fetchCorpusDocuments,
  fetchCorpusJobs,
  fetchCorpusLibraries,
  fetchCorpusUnit,
  fetchCorpusUnits,
  fetchProjectCorpusLibraries,
  importCorpusFromRoot,
  rebuildCorpus,
  searchCorpus,
  updateCorpusDocument,
  updateCorpusLibrary,
  updateProjectCorpusLibraries,
  uploadCorpus,
} from "../api";
import type { CorpusDocument, CorpusJob } from "../types";

import "./corpus-page.css";

const PROJECT_PAGE_SIZE = 100;
const LIBRARY_SEARCH_SCOPE = "__library__";
const DISABLED_MODEL_VALUE = "__disabled__";

function errorDetail(error: unknown, fallback: string): string {
  if (!axios.isAxiosError(error)) return fallback;
  const detail = error.response?.data?.detail;
  return typeof detail === "string" && detail ? detail : fallback;
}

function splitTags(value: string): string[] {
  return value
    .split(/[,，]/)
    .map((tag) => tag.trim())
    .filter((tag, index, tags) => tag && tags.indexOf(tag) === index);
}

function formatNumber(value: number): string {
  return new Intl.NumberFormat().format(value);
}

function jobStatusColor(status: string): "gray" | "blue" | "green" | "red" | "amber" {
  if (status === "running") return "blue";
  if (status === "succeeded") return "green";
  if (status === "failed" || status === "timeout") return "red";
  if (status === "paused") return "amber";
  return "gray";
}

export function CorpusPage() {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const uploadInputRef = useRef<HTMLInputElement>(null);
  const pendingSearchTargetRef = useRef<{
    libraryId: string;
    documentId: string;
    unitId: string;
  } | null>(null);

  const [selectedLibraryId, setSelectedLibraryId] = useState("");
  const [selectedDocumentId, setSelectedDocumentId] = useState("");
  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [mountSelection, setMountSelection] = useState<string[]>([]);
  const [newLibraryName, setNewLibraryName] = useState("");
  const [libraryName, setLibraryName] = useState("");
  const [libraryDescription, setLibraryDescription] = useState("");
  const [libraryTags, setLibraryTags] = useState("");
  const [documentTitle, setDocumentTitle] = useState("");
  const [documentAuthor, setDocumentAuthor] = useState("");
  const [documentDynasty, setDocumentDynasty] = useState("");
  const [documentTags, setDocumentTags] = useState("");
  const [documentMetadata, setDocumentMetadata] = useState("{}");
  const [rootPath, setRootPath] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [searchScope, setSearchScope] = useState(LIBRARY_SEARCH_SCOPE);
  const [readUnitId, setReadUnitId] = useState("");
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [pendingEmbeddingModel, setPendingEmbeddingModel] = useState<string | null>(null);

  const librariesQuery = useQuery({
    queryKey: ["corpus", "libraries"],
    queryFn: fetchCorpusLibraries,
  });
  const libraries = useMemo(() => librariesQuery.data ?? [], [librariesQuery.data]);
  const selectedLibrary = libraries.find((library) => library.id === selectedLibraryId) ?? null;

  const documentsQuery = useQuery({
    queryKey: ["corpus", "documents", selectedLibraryId],
    queryFn: () => fetchCorpusDocuments(selectedLibraryId),
    enabled: Boolean(selectedLibraryId),
  });
  const documents = useMemo(() => documentsQuery.data ?? [], [documentsQuery.data]);
  const selectedDocument = documents.find((document) => document.id === selectedDocumentId) ?? null;

  const unitsQuery = useQuery({
    queryKey: ["corpus", "units", selectedDocumentId],
    queryFn: () => fetchCorpusUnits(selectedDocumentId),
    enabled: Boolean(selectedDocumentId),
  });
  const unitQuery = useQuery({
    queryKey: ["corpus", "unit", readUnitId],
    queryFn: () => fetchCorpusUnit(readUnitId),
    enabled: Boolean(readUnitId),
  });
  const projectsQuery = useQuery({
    queryKey: ["projects", "corpus-mount-options"],
    queryFn: () => fetchProjects({ page: 1, pageSize: PROJECT_PAGE_SIZE }),
  });
  const projects = useMemo(() => projectsQuery.data?.items ?? [], [projectsQuery.data?.items]);
  const mountsQuery = useQuery({
    queryKey: ["corpus", "mounts", selectedProjectId],
    queryFn: () => fetchProjectCorpusLibraries(selectedProjectId),
    enabled: Boolean(selectedProjectId),
  });
  const jobsQuery = useQuery({
    queryKey: ["corpus", "jobs"],
    queryFn: fetchCorpusJobs,
    refetchInterval: 3000,
  });
  const settingsQuery = useQuery({
    queryKey: ["settings"],
    queryFn: fetchSettings,
  });
  const embeddingModelsQuery = useQuery({
    queryKey: ["models", "embedding"],
    queryFn: () => fetchModels(undefined, "embedding"),
  });
  const rerankModelsQuery = useQuery({
    queryKey: ["models", "rerank"],
    queryFn: () => fetchModels(undefined, "rerank"),
  });
  const agentSettingsLockQuery = useAgentSettingsLock();

  useEffect(() => {
    if (selectedLibraryId && libraries.some((item) => item.id === selectedLibraryId)) return;
    setSelectedLibraryId(libraries[0]?.id ?? "");
  }, [libraries, selectedLibraryId]);

  useEffect(() => {
    const pendingTarget = pendingSearchTargetRef.current;
    if (pendingTarget?.libraryId === selectedLibraryId) {
      if (documents.some((item) => item.id === pendingTarget.documentId)) {
        pendingSearchTargetRef.current = null;
        setSelectedDocumentId(pendingTarget.documentId);
        setReadUnitId(pendingTarget.unitId);
        return;
      }
      if (documentsQuery.isFetching) return;
      pendingSearchTargetRef.current = null;
    }
    if (selectedDocumentId && documents.some((item) => item.id === selectedDocumentId)) return;
    setSelectedDocumentId(documents[0]?.id ?? "");
    setReadUnitId("");
  }, [documents, documentsQuery.isFetching, selectedDocumentId, selectedLibraryId]);

  useEffect(() => {
    if (!selectedLibrary) return;
    setLibraryName(selectedLibrary.name);
    setLibraryDescription(selectedLibrary.description ?? "");
    setLibraryTags(selectedLibrary.tags.join(", "));
  }, [selectedLibrary]);

  useEffect(() => {
    if (!selectedDocument) return;
    setDocumentTitle(selectedDocument.title);
    setDocumentAuthor(selectedDocument.author ?? "");
    setDocumentDynasty(selectedDocument.dynasty ?? "");
    setDocumentTags(selectedDocument.tags.join(", "));
    setDocumentMetadata(JSON.stringify(selectedDocument.metadata, null, 2));
  }, [selectedDocument]);

  useEffect(() => {
    setMountSelection(mountsQuery.data ?? []);
  }, [mountsQuery.data]);

  const refreshCorpus = async (libraryId?: string) => {
    await Promise.all([
      queryClient.invalidateQueries({ queryKey: ["corpus", "libraries"] }),
      queryClient.invalidateQueries({
        queryKey: ["corpus", "documents", libraryId ?? selectedLibraryId],
      }),
      queryClient.invalidateQueries({ queryKey: ["corpus", "jobs"] }),
    ]);
  };

  const createLibraryMutation = useMutation({
    mutationFn: () => createCorpusLibrary({ name: newLibraryName }),
    onSuccess: async (library) => {
      setNewLibraryName("");
      setSelectedLibraryId(library.id);
      await refreshCorpus(library.id);
      toast.success(t("corpus.libraryCreated"));
    },
    onError: (error) => toast.error(errorDetail(error, t("corpus.operationFailed"))),
  });
  const updateLibraryMutation = useMutation({
    mutationFn: () =>
      updateCorpusLibrary(selectedLibraryId, {
        name: libraryName,
        description: libraryDescription,
        tags: splitTags(libraryTags),
      }),
    onSuccess: async () => {
      await refreshCorpus();
      toast.success(t("common.saveSuccess"));
    },
    onError: (error) => toast.error(errorDetail(error, t("common.saveFailed"))),
  });
  const deleteLibraryMutation = useMutation({
    mutationFn: () => deleteCorpusLibrary(selectedLibraryId),
    onSuccess: async () => {
      setDeleteDialogOpen(false);
      setSelectedLibraryId("");
      await refreshCorpus();
      toast.success(t("common.deleteSuccess"));
    },
    onError: (error) => toast.error(errorDetail(error, t("common.deleteFailed"))),
  });
  const updateDocumentMutation = useMutation({
    mutationFn: () => {
      let metadata: Record<string, unknown>;
      try {
        const parsed: unknown = JSON.parse(documentMetadata || "{}");
        if (!parsed || Array.isArray(parsed) || typeof parsed !== "object") throw new Error();
        metadata = parsed as Record<string, unknown>;
      } catch {
        throw new Error(t("corpus.invalidMetadata"));
      }
      return updateCorpusDocument(selectedDocumentId, {
        title: documentTitle,
        author: documentAuthor,
        dynasty: documentDynasty,
        tags: splitTags(documentTags),
        metadata,
      });
    },
    onSuccess: async () => {
      await refreshCorpus();
      toast.success(t("common.saveSuccess"));
    },
    onError: (error) =>
      toast.error(error instanceof Error ? error.message : t("common.saveFailed")),
  });
  const importMutation = useMutation({
    mutationFn: (file: File) => uploadCorpus(file, selectedLibraryId || undefined),
    onSuccess: async (result) => {
      setSelectedLibraryId(result.libraryId);
      await refreshCorpus(result.libraryId);
      toast.success(
        t("corpus.importComplete", {
          imported: result.importedCount,
          deduplicated: result.deduplicatedCount,
        }),
      );
    },
    onError: (error) => toast.error(errorDetail(error, t("corpus.importFailed"))),
  });
  const rootImportMutation = useMutation({
    mutationFn: () => importCorpusFromRoot(rootPath, selectedLibraryId || undefined),
    onSuccess: async (result) => {
      setRootPath("");
      setSelectedLibraryId(result.libraryId);
      await refreshCorpus(result.libraryId);
      toast.success(t("corpus.importQueued"));
    },
    onError: (error) => toast.error(errorDetail(error, t("corpus.importFailed"))),
  });
  const mountMutation = useMutation({
    mutationFn: () => updateProjectCorpusLibraries(selectedProjectId, mountSelection),
    onSuccess: async (ids) => {
      setMountSelection(ids);
      await queryClient.invalidateQueries({
        queryKey: ["corpus", "mounts", selectedProjectId],
      });
      toast.success(t("corpus.mountSaved"));
    },
    onError: (error) => toast.error(errorDetail(error, t("common.saveFailed"))),
  });
  const searchMutation = useMutation({
    mutationFn: () =>
      searchCorpus({
        query: searchQuery,
        projectId: searchScope === LIBRARY_SEARCH_SCOPE ? undefined : searchScope,
        libraryIds:
          searchScope === LIBRARY_SEARCH_SCOPE && selectedLibraryId
            ? [selectedLibraryId]
            : undefined,
      }),
    onError: (error) => toast.error(errorDetail(error, t("corpus.searchFailed"))),
  });
  const rebuildMutation = useMutation({
    mutationFn: rebuildCorpus,
    onSuccess: async (result) => {
      await refreshCorpus();
      toast.success(t("corpus.rebuildQueued", { count: result.documentCount }));
    },
    onError: (error) => toast.error(errorDetail(error, t("corpus.operationFailed"))),
  });
  const jobMutation = useMutation({
    mutationFn: ({ job, action }: { job: CorpusJob; action: JobAction }) =>
      controlCorpusJob(job.id, action),
    onSuccess: async () => {
      await refreshCorpus();
    },
    onError: (error) => toast.error(errorDetail(error, t("corpus.operationFailed"))),
  });
  const settingsMutation = useMutation({
    mutationFn: updateSettings,
    onSuccess: (settings) => {
      queryClient.setQueryData(["settings"], settings);
      toast.success(t("common.saveSuccess"));
    },
    onError: (error) => toast.error(errorDetail(error, t("common.saveFailed"))),
  });

  const projectOptions = useMemo(
    () => projects.map((project) => ({ value: project.id, label: project.title })),
    [projects],
  );
  const searchScopeOptions = useMemo(
    () => [{ value: LIBRARY_SEARCH_SCOPE, label: t("corpus.currentLibrary") }, ...projectOptions],
    [projectOptions, t],
  );
  const embeddingModelOptions = useMemo(
    () => [
      { value: DISABLED_MODEL_VALUE, label: t("corpus.disabled") },
      ...(embeddingModelsQuery.data ?? []).map((model) => ({
        value: model.id,
        label: model.name || model.modelId,
        description: model.name === model.modelId ? undefined : model.modelId,
      })),
    ],
    [embeddingModelsQuery.data, t],
  );
  const rerankModelOptions = useMemo(
    () => [
      { value: DISABLED_MODEL_VALUE, label: t("corpus.disabled") },
      ...(rerankModelsQuery.data ?? []).map((model) => ({
        value: model.id,
        label: model.name || model.modelId,
        description: model.name === model.modelId ? undefined : model.modelId,
      })),
    ],
    [rerankModelsQuery.data, t],
  );
  const concurrencyOptions = useMemo(
    () =>
      [1, 2, 3, 4].map((value) => ({
        value: String(value),
        label: t("corpus.concurrencyValue", { value }),
      })),
    [t],
  );

  const saveEmbeddingModel = (modelId: string) => {
    settingsMutation.mutate({ corpus_embedding_model: modelId });
  };

  const handleEmbeddingModelChange = (value: string) => {
    const nextModel = value === DISABLED_MODEL_VALUE ? "" : value;
    const currentModel = settingsQuery.data?.corpusEmbeddingModel ?? "";
    if (currentModel && currentModel !== nextModel) {
      setPendingEmbeddingModel(nextModel);
      return;
    }
    saveEmbeddingModel(nextModel);
  };

  const handleRerankModelChange = (value: string) => {
    const modelId = value === DISABLED_MODEL_VALUE ? "" : value;
    settingsMutation.mutate({
      corpus_rerank_enabled: Boolean(modelId),
      corpus_rerank_model: modelId,
    });
  };

  const toggleMountedLibrary = (libraryId: string, checked: boolean) => {
    setMountSelection((current) =>
      checked
        ? [...current, libraryId].filter((id, index, ids) => ids.indexOf(id) === index)
        : current.filter((id) => id !== libraryId),
    );
  };

  return (
    <Box className="corpus-page">
      <header className="corpus-header">
        <Flex
          align="center"
          gap="3"
          className="corpus-header-main"
        >
          <MobileAppSidebarTrigger />
          <BookOpen
            size={20}
            aria-hidden="true"
          />
          <Heading size="4">{t("corpus.title")}</Heading>
        </Flex>
        <Flex
          align="center"
          gap="2"
          wrap="wrap"
          className="corpus-header-actions"
        >
          <input
            ref={uploadInputRef}
            type="file"
            accept=".zip,.txt"
            hidden
            onChange={(event) => {
              const file = event.target.files?.[0];
              if (file) importMutation.mutate(file);
              event.target.value = "";
            }}
          />
          <Button
            variant="soft"
            color="gray"
            onClick={() => uploadInputRef.current?.click()}
            loading={importMutation.isPending}
          >
            <Upload size={16} />
            {t("corpus.upload")}
          </Button>
          <Button
            variant="soft"
            color="gray"
            onClick={() => rebuildMutation.mutate()}
            loading={rebuildMutation.isPending}
            disabled={!settingsQuery.data?.corpusEmbeddingModel}
          >
            <RefreshCw size={16} />
            {t("corpus.rebuild")}
          </Button>
        </Flex>
      </header>

      <div className="corpus-workspace">
        <aside className="corpus-libraries-panel">
          <div className="corpus-panel-heading">
            <Text
              size="2"
              weight="bold"
            >
              {t("corpus.libraries")}
            </Text>
            <Text
              size="1"
              color="gray"
            >
              {libraries.length}
            </Text>
          </div>
          <Flex
            gap="2"
            p="3"
            className="corpus-create-library"
          >
            <TextField.Root
              value={newLibraryName}
              placeholder={t("corpus.newLibrary")}
              onChange={(event) => setNewLibraryName(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter" && newLibraryName.trim()) {
                  createLibraryMutation.mutate();
                }
              }}
            />
            <Tooltip content={t("common.create")}>
              <Button
                aria-label={t("common.create")}
                variant="soft"
                color="gray"
                className="corpus-icon-button"
                disabled={!newLibraryName.trim()}
                loading={createLibraryMutation.isPending}
                onClick={() => createLibraryMutation.mutate()}
              >
                <Plus size={16} />
              </Button>
            </Tooltip>
          </Flex>
          <div className="corpus-library-list">
            {librariesQuery.isLoading ? (
              <Flex
                justify="center"
                p="5"
              >
                <Spinner size={18} />
              </Flex>
            ) : null}
            {!librariesQuery.isLoading && libraries.length === 0 ? (
              <Text
                size="2"
                color="gray"
                className="corpus-empty-copy"
              >
                {t("corpus.noLibraries")}
              </Text>
            ) : null}
            {libraries.map((library) => (
              <button
                type="button"
                key={library.id}
                className="corpus-library-row"
                data-active={library.id === selectedLibraryId}
                onClick={() => setSelectedLibraryId(library.id)}
              >
                <span className="corpus-library-name">{library.name}</span>
                <span className="corpus-library-count">{library.documentCount}</span>
              </button>
            ))}
          </div>
        </aside>

        <main className="corpus-main-panel">
          {!selectedLibrary ? (
            <EmptyState text={t("corpus.selectLibrary")} />
          ) : (
            <>
              <section className="corpus-library-editor">
                <div className="corpus-section-title-row">
                  <div>
                    <Heading size="3">{selectedLibrary.name}</Heading>
                    <Text
                      size="1"
                      color="gray"
                    >
                      {t("corpus.libraryStats", {
                        documents: selectedLibrary.documentCount,
                        characters: formatNumber(selectedLibrary.charCount),
                      })}
                    </Text>
                  </div>
                  <Flex gap="2">
                    <Button
                      size="2"
                      variant="soft"
                      color="gray"
                      onClick={() => updateLibraryMutation.mutate()}
                      loading={updateLibraryMutation.isPending}
                    >
                      <Save size={15} />
                      {t("common.save")}
                    </Button>
                    <Tooltip content={t("common.delete")}>
                      <Button
                        size="2"
                        variant="ghost"
                        color="red"
                        className="corpus-icon-button"
                        aria-label={t("common.delete")}
                        onClick={() => setDeleteDialogOpen(true)}
                      >
                        <Trash2 size={16} />
                      </Button>
                    </Tooltip>
                  </Flex>
                </div>
                <div className="corpus-form-grid corpus-form-grid--library">
                  <Field label={t("corpus.name")}>
                    <TextField.Root
                      value={libraryName}
                      onChange={(event) => setLibraryName(event.target.value)}
                    />
                  </Field>
                  <Field label={t("corpus.tags")}>
                    <TextField.Root
                      value={libraryTags}
                      onChange={(event) => setLibraryTags(event.target.value)}
                    />
                  </Field>
                  <Field
                    label={t("corpus.description")}
                    wide
                  >
                    <TextArea
                      value={libraryDescription}
                      resize="vertical"
                      rows={2}
                      onChange={(event) => setLibraryDescription(event.target.value)}
                    />
                  </Field>
                </div>
                <Flex
                  gap="2"
                  className="corpus-root-import"
                >
                  <TextField.Root
                    value={rootPath}
                    placeholder={t("corpus.importPath")}
                    onChange={(event) => setRootPath(event.target.value)}
                  >
                    <TextField.Slot>
                      <FolderInput size={15} />
                    </TextField.Slot>
                  </TextField.Root>
                  <Button
                    variant="soft"
                    color="gray"
                    disabled={!rootPath.trim()}
                    loading={rootImportMutation.isPending}
                    onClick={() => rootImportMutation.mutate()}
                  >
                    {t("common.import")}
                  </Button>
                </Flex>
              </section>

              <section className="corpus-documents-section">
                <div className="corpus-panel-heading corpus-panel-heading--main">
                  <Text
                    size="2"
                    weight="bold"
                  >
                    {t("corpus.documents")}
                  </Text>
                  <Text
                    size="1"
                    color="gray"
                  >
                    {documents.length}
                  </Text>
                </div>
                {documentsQuery.isLoading ? (
                  <Flex
                    justify="center"
                    p="5"
                  >
                    <Spinner size={18} />
                  </Flex>
                ) : null}
                {!documentsQuery.isLoading && documents.length === 0 ? (
                  <EmptyState
                    text={t("corpus.noDocuments")}
                    compact
                  />
                ) : (
                  <div className="corpus-document-list">
                    {documents.map((document) => (
                      <DocumentRow
                        key={document.id}
                        document={document}
                        active={document.id === selectedDocumentId}
                        onClick={() => {
                          setSelectedDocumentId(document.id);
                          setReadUnitId("");
                        }}
                        t={t}
                      />
                    ))}
                  </div>
                )}
              </section>

              {selectedDocument ? (
                <section className="corpus-document-editor">
                  <div className="corpus-section-title-row">
                    <div>
                      <Heading size="3">{selectedDocument.title}</Heading>
                      <Flex
                        gap="2"
                        align="center"
                        mt="1"
                      >
                        <Badge color={indexStatusColor(selectedDocument.indexStatus)}>
                          {t(`corpus.indexStatus.${selectedDocument.indexStatus}`, {
                            defaultValue: selectedDocument.indexStatus,
                          })}
                        </Badge>
                        <Text
                          size="1"
                          color="gray"
                        >
                          {t("corpus.documentStats", {
                            units: selectedDocument.unitCount,
                            characters: formatNumber(selectedDocument.charCount),
                          })}
                        </Text>
                      </Flex>
                    </div>
                    <Button
                      variant="soft"
                      color="gray"
                      onClick={() => updateDocumentMutation.mutate()}
                      loading={updateDocumentMutation.isPending}
                    >
                      <Save size={15} />
                      {t("common.save")}
                    </Button>
                  </div>
                  <div className="corpus-form-grid">
                    <Field label={t("corpus.titleLabel")}>
                      <TextField.Root
                        value={documentTitle}
                        onChange={(event) => setDocumentTitle(event.target.value)}
                      />
                    </Field>
                    <Field label={t("corpus.author")}>
                      <TextField.Root
                        value={documentAuthor}
                        onChange={(event) => setDocumentAuthor(event.target.value)}
                      />
                    </Field>
                    <Field label={t("corpus.dynasty")}>
                      <TextField.Root
                        value={documentDynasty}
                        onChange={(event) => setDocumentDynasty(event.target.value)}
                      />
                    </Field>
                    <Field label={t("corpus.tags")}>
                      <TextField.Root
                        value={documentTags}
                        onChange={(event) => setDocumentTags(event.target.value)}
                      />
                    </Field>
                    <Field
                      label={t("corpus.metadata")}
                      wide
                    >
                      <TextArea
                        className="corpus-metadata-input"
                        value={documentMetadata}
                        rows={5}
                        resize="vertical"
                        onChange={(event) => setDocumentMetadata(event.target.value)}
                      />
                    </Field>
                  </div>

                  <div className="corpus-units-block">
                    <Text
                      size="2"
                      weight="bold"
                    >
                      {t("corpus.units")}
                    </Text>
                    <div className="corpus-unit-list">
                      {(unitsQuery.data ?? []).map((unit) => (
                        <button
                          type="button"
                          key={unit.id}
                          className="corpus-unit-row"
                          data-active={unit.id === readUnitId}
                          onClick={() => setReadUnitId(unit.id)}
                        >
                          <FileText
                            size={14}
                            aria-hidden="true"
                          />
                          <span>{unit.title || `${unit.kind} ${unit.order + 1}`}</span>
                          <span>{formatNumber(unit.charCount)}</span>
                        </button>
                      ))}
                    </div>
                    {unitQuery.isFetching ? (
                      <Flex
                        justify="center"
                        p="4"
                      >
                        <Spinner size={18} />
                      </Flex>
                    ) : null}
                    {unitQuery.data ? (
                      <div className="corpus-unit-reader">
                        <Flex
                          justify="between"
                          align="center"
                          gap="2"
                        >
                          <Text
                            size="2"
                            weight="bold"
                          >
                            {unitQuery.data.title || unitQuery.data.documentTitle}
                          </Text>
                          <Tooltip content={t("common.close")}>
                            <Button
                              variant="ghost"
                              color="gray"
                              className="corpus-icon-button"
                              aria-label={t("common.close")}
                              onClick={() => setReadUnitId("")}
                            >
                              <X size={15} />
                            </Button>
                          </Tooltip>
                        </Flex>
                        <pre>{unitQuery.data.text}</pre>
                      </div>
                    ) : null}
                  </div>
                </section>
              ) : null}
            </>
          )}
        </main>

        <aside className="corpus-operations-panel">
          <Tabs.Root defaultValue="mounts">
            <Tabs.List className="corpus-tabs-list">
              <Tabs.Trigger value="mounts">{t("corpus.mounts")}</Tabs.Trigger>
              <Tabs.Trigger value="search">{t("corpus.search")}</Tabs.Trigger>
              <Tabs.Trigger value="jobs">{t("corpus.jobs")}</Tabs.Trigger>
              <Tabs.Trigger
                value="settings"
                aria-label={t("corpus.settings")}
              >
                <SlidersHorizontal size={14} />
              </Tabs.Trigger>
            </Tabs.List>
            <Tabs.Content
              value="mounts"
              className="corpus-tab-content"
            >
              <LabeledSelect
                label={t("corpus.project")}
                value={selectedProjectId}
                options={projectOptions}
                placeholder={t("corpus.selectProject")}
                onChange={setSelectedProjectId}
                triggerStyle={{ width: "100%" }}
              />
              <div className="corpus-mount-list">
                {libraries.map((library) => (
                  <label
                    key={library.id}
                    className="corpus-checkbox-row"
                  >
                    <Checkbox
                      checked={mountSelection.includes(library.id)}
                      disabled={!selectedProjectId}
                      onCheckedChange={(checked) =>
                        toggleMountedLibrary(library.id, checked === true)
                      }
                    />
                    <span>{library.name}</span>
                  </label>
                ))}
              </div>
              <Button
                className="corpus-full-button"
                disabled={!selectedProjectId}
                loading={mountMutation.isPending}
                onClick={() => mountMutation.mutate()}
              >
                <Save size={15} />
                {t("common.save")}
              </Button>
            </Tabs.Content>

            <Tabs.Content
              value="search"
              className="corpus-tab-content"
            >
              <LabeledSelect
                label={t("corpus.scope")}
                value={searchScope}
                options={searchScopeOptions}
                onChange={setSearchScope}
                triggerStyle={{ width: "100%" }}
              />
              <TextArea
                value={searchQuery}
                rows={3}
                resize="vertical"
                placeholder={t("corpus.searchPlaceholder")}
                onChange={(event) => setSearchQuery(event.target.value)}
              />
              <Button
                className="corpus-full-button"
                disabled={
                  !searchQuery.trim() ||
                  (searchScope === LIBRARY_SEARCH_SCOPE && !selectedLibraryId)
                }
                loading={searchMutation.isPending}
                onClick={() => searchMutation.mutate()}
              >
                <Search size={15} />
                {t("corpus.search")}
              </Button>
              <div className="corpus-search-results">
                {(searchMutation.data ?? []).map((hit) => (
                  <button
                    type="button"
                    key={`${hit.unitId}-${hit.chunkIndex}`}
                    className="corpus-search-hit"
                    onClick={() => {
                      const libraryId = hit.libraryIds.find((id) =>
                        libraries.some((library) => library.id === id),
                      );
                      if (libraryId && libraryId !== selectedLibraryId) {
                        pendingSearchTargetRef.current = {
                          libraryId,
                          documentId: hit.documentId,
                          unitId: hit.unitId,
                        };
                        setSelectedLibraryId(libraryId);
                        return;
                      }
                      setSelectedDocumentId(hit.documentId);
                      setReadUnitId(hit.unitId);
                    }}
                  >
                    <span className="corpus-search-hit-title">
                      {hit.title}
                      {hit.unitTitle ? ` · ${hit.unitTitle}` : ""}
                    </span>
                    <span className="corpus-search-hit-meta">
                      {[hit.dynasty, hit.author, hit.matchedBy].filter(Boolean).join(" · ")}
                    </span>
                    <span className="corpus-search-hit-text">{hit.contextText || hit.text}</span>
                  </button>
                ))}
                {searchMutation.isSuccess && searchMutation.data.length === 0 ? (
                  <Text
                    size="2"
                    color="gray"
                    className="corpus-empty-copy"
                  >
                    {t("corpus.noResults")}
                  </Text>
                ) : null}
              </div>
            </Tabs.Content>

            <Tabs.Content
              value="jobs"
              className="corpus-tab-content corpus-tab-content--jobs"
            >
              {(jobsQuery.data ?? []).map((job) => (
                <JobRow
                  key={job.id}
                  job={job}
                  pending={jobMutation.isPending}
                  onAction={(action) => jobMutation.mutate({ job, action })}
                  t={t}
                />
              ))}
              {!jobsQuery.isLoading && (jobsQuery.data?.length ?? 0) === 0 ? (
                <Text
                  size="2"
                  color="gray"
                  className="corpus-empty-copy"
                >
                  {t("corpus.noJobs")}
                </Text>
              ) : null}
            </Tabs.Content>

            <Tabs.Content
              value="settings"
              className="corpus-tab-content"
            >
              {agentSettingsLockQuery.data ? (
                <Text
                  size="2"
                  color="amber"
                >
                  {t("settings.agentSettingsLocked")} {t("settings.agentSettingsLockHint")}
                </Text>
              ) : null}
              {settingsQuery.isLoading ||
              embeddingModelsQuery.isLoading ||
              rerankModelsQuery.isLoading ? (
                <Flex
                  justify="center"
                  p="5"
                >
                  <Spinner size={18} />
                </Flex>
              ) : settingsQuery.data ? (
                <>
                  <LabeledSelect
                    label={t("corpus.embeddingModel")}
                    value={settingsQuery.data.corpusEmbeddingModel || DISABLED_MODEL_VALUE}
                    options={embeddingModelOptions}
                    onChange={handleEmbeddingModelChange}
                    triggerStyle={{ width: "100%" }}
                    disabled={agentSettingsLockQuery.data || settingsMutation.isPending}
                  />
                  <LabeledSelect
                    label={t("corpus.rerankModel")}
                    value={
                      settingsQuery.data.corpusRerankEnabled
                        ? settingsQuery.data.corpusRerankModel || DISABLED_MODEL_VALUE
                        : DISABLED_MODEL_VALUE
                    }
                    options={rerankModelOptions}
                    onChange={handleRerankModelChange}
                    triggerStyle={{ width: "100%" }}
                    disabled={agentSettingsLockQuery.data || settingsMutation.isPending}
                  />
                  <LabeledSelect
                    label={t("corpus.indexConcurrency")}
                    value={String(settingsQuery.data.corpusIndexConcurrency)}
                    options={concurrencyOptions}
                    onChange={(value) =>
                      settingsMutation.mutate({ corpus_index_concurrency: Number(value) })
                    }
                    triggerStyle={{ width: "100%" }}
                    disabled={agentSettingsLockQuery.data || settingsMutation.isPending}
                  />
                </>
              ) : (
                <Text
                  size="2"
                  color="gray"
                  className="corpus-empty-copy"
                >
                  {t("corpus.settingsLoadFailed")}
                </Text>
              )}
            </Tabs.Content>
          </Tabs.Root>
        </aside>
      </div>

      <ConfirmDialog
        open={deleteDialogOpen}
        onOpenChange={setDeleteDialogOpen}
        onConfirm={() => deleteLibraryMutation.mutate()}
        title={t("corpus.deleteLibrary")}
        description={t("corpus.deleteLibraryConfirm", { name: selectedLibrary?.name ?? "" })}
        loading={deleteLibraryMutation.isPending}
      />
      <ConfirmDialog
        open={pendingEmbeddingModel !== null}
        onOpenChange={(open) => {
          if (!open) setPendingEmbeddingModel(null);
        }}
        onConfirm={() => {
          if (pendingEmbeddingModel === null) return;
          saveEmbeddingModel(pendingEmbeddingModel);
          setPendingEmbeddingModel(null);
        }}
        title={t("corpus.embeddingModelChangeTitle")}
        description={t("corpus.embeddingModelChangeConfirm")}
        confirmText={t("common.confirm")}
        confirmColor="blue"
        loading={settingsMutation.isPending}
      />
    </Box>
  );
}

function Field({
  label,
  wide = false,
  children,
}: {
  label: string;
  wide?: boolean;
  children: React.ReactNode;
}) {
  return (
    <label className={wide ? "corpus-field corpus-field--wide" : "corpus-field"}>
      <Text
        size="1"
        color="gray"
      >
        {label}
      </Text>
      {children}
    </label>
  );
}

function EmptyState({ text, compact = false }: { text: string; compact?: boolean }) {
  return (
    <Flex
      align="center"
      justify="center"
      className={compact ? "corpus-empty corpus-empty--compact" : "corpus-empty"}
    >
      <Text
        size="2"
        color="gray"
      >
        {text}
      </Text>
    </Flex>
  );
}

function DocumentRow({
  document,
  active,
  onClick,
  t,
}: {
  document: CorpusDocument;
  active: boolean;
  onClick: () => void;
  t: (key: string, options?: Record<string, unknown>) => string;
}) {
  return (
    <button
      type="button"
      className="corpus-document-row"
      data-active={active}
      onClick={onClick}
    >
      <FileText
        size={16}
        aria-hidden="true"
      />
      <span className="corpus-document-row-main">
        <span className="corpus-document-row-title">{document.title}</span>
        <span className="corpus-document-row-meta">
          {[document.dynasty, document.author, document.kind].filter(Boolean).join(" · ")}
        </span>
      </span>
      <span className="corpus-document-row-status">
        {t(`corpus.indexStatus.${document.indexStatus}`, {
          defaultValue: document.indexStatus,
        })}
      </span>
    </button>
  );
}

type JobAction = "pause" | "resume" | "cancel" | "retry";

function JobRow({
  job,
  pending,
  onAction,
  t,
}: {
  job: CorpusJob;
  pending: boolean;
  onAction: (action: JobAction) => void;
  t: (key: string, options?: Record<string, unknown>) => string;
}) {
  const current = Number(job.progress.current ?? 0);
  const total = Number(job.progress.total ?? 0);
  const message = typeof job.progress.message === "string" ? job.progress.message : "";
  const error = typeof job.error.message === "string" ? job.error.message : "";
  return (
    <div className="corpus-job-row">
      <Flex
        justify="between"
        align="center"
        gap="2"
      >
        <Badge color={jobStatusColor(job.status)}>
          {t(`corpus.jobStatus.${job.status}`, { defaultValue: job.status })}
        </Badge>
        <Flex gap="1">
          {(job.status === "running" || job.status === "pending") && (
            <JobButton
              label={t("corpus.pause")}
              onClick={() => onAction("pause")}
              disabled={pending}
            >
              <Pause size={14} />
            </JobButton>
          )}
          {job.status === "paused" && (
            <JobButton
              label={t("corpus.resume")}
              onClick={() => onAction("resume")}
              disabled={pending}
            >
              <Play size={14} />
            </JobButton>
          )}
          {(["failed", "timeout", "cancelled"] as string[]).includes(job.status) && (
            <JobButton
              label={t("corpus.retry")}
              onClick={() => onAction("retry")}
              disabled={pending}
            >
              <RotateCcw size={14} />
            </JobButton>
          )}
          {(["running", "pending", "paused"] as string[]).includes(job.status) && (
            <JobButton
              label={t("common.cancel")}
              onClick={() => onAction("cancel")}
              disabled={pending}
            >
              <X size={14} />
            </JobButton>
          )}
        </Flex>
      </Flex>
      <Text
        size="1"
        color="gray"
        className="corpus-job-id"
      >
        {job.id}
      </Text>
      {total > 0 ? (
        <div
          className="corpus-job-progress"
          aria-label={`${current}/${total}`}
        >
          <span style={{ width: `${Math.min(100, (current / total) * 100)}%` }} />
        </div>
      ) : null}
      {message ? <Text size="1">{message}</Text> : null}
      {error ? (
        <Text
          size="1"
          color="red"
        >
          {error}
        </Text>
      ) : null}
    </div>
  );
}

function JobButton({
  label,
  onClick,
  disabled,
  children,
}: {
  label: string;
  onClick: () => void;
  disabled: boolean;
  children: React.ReactNode;
}) {
  return (
    <Tooltip content={label}>
      <Button
        size="1"
        variant="ghost"
        color="gray"
        className="corpus-job-button"
        aria-label={label}
        disabled={disabled}
        onClick={onClick}
      >
        {children}
      </Button>
    </Tooltip>
  );
}

function indexStatusColor(status: string): "gray" | "blue" | "green" | "red" | "amber" {
  if (status === "ready") return "green";
  if (status === "queued" || status === "indexing") return "blue";
  if (status === "failed") return "red";
  if (status === "needs_rebuild") return "amber";
  return "gray";
}
