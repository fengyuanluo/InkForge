import { Box, Text } from "@radix-ui/themes";

import i18n from "@/i18n";
import type { AgentMessage } from "@/lib/agent.types";

import {
  ToolBody,
  ToolGroup,
  ToolListBlock,
  ToolNotice,
  ToolPanel,
  ToolTextBlock,
} from "../shared/tool-message-shared";
import { asString, getToolResultRecord, isRecord } from "../shared/tool-message-utils";

import "./novel-research-tool-message.css";

interface NovelResearchToolMessageProps {
  message: AgentMessage;
}

function displayValue(value: unknown): string | undefined {
  if (typeof value === "string" || typeof value === "number") return String(value);
  if (value === null || value === undefined) return undefined;
  try {
    return JSON.stringify(value, null, 2);
  } catch {
    return String(value);
  }
}

function metricLabel(key: string): string {
  const labels: Record<string, string> = {
    reading_count: i18n.t("assistant.tools.readingCount"),
    favorite_count: i18n.t("assistant.tools.favoriteCount"),
    recommendation_count: i18n.t("assistant.tools.recommendationCount"),
    comment_count: i18n.t("assistant.tools.commentCount"),
    rating: i18n.t("assistant.tools.rating"),
    hot_score: i18n.t("assistant.tools.hotScore"),
    rank_metric: i18n.t("assistant.tools.rankMetric"),
  };
  return labels[key] ?? key;
}

function Metrics({ metrics }: { metrics: Record<string, unknown> }) {
  const entries = Object.entries(metrics).filter(
    ([, value]) => value !== null && value !== undefined,
  );
  return (
    <ToolGroup label={i18n.t("assistant.tools.novelMetrics")}>
      {entries.length > 0 ? (
        <Box className="agent-tool-content-value agent-tool-content-plain-text">
          {entries.map(([key, value]) => (
            <Box key={key}>
              <strong>{metricLabel(key)}</strong>: {displayValue(value)}
            </Box>
          ))}
        </Box>
      ) : (
        <Text
          size="2"
          color="gray"
        >
          {i18n.t("assistant.tools.noPublicMetrics")}
        </Text>
      )}
    </ToolGroup>
  );
}

function BookCard({
  book,
  rank,
  rankMetric,
}: {
  book: Record<string, unknown>;
  rank?: unknown;
  rankMetric?: unknown;
}) {
  const metrics = { ...(isRecord(book.metrics) ? book.metrics : {}) };
  if (metrics.rank_metric === null || metrics.rank_metric === undefined) {
    metrics.rank_metric = rankMetric;
  }
  const sourceExtra = isRecord(book.source_extra) ? book.source_extra : {};
  return (
    <ToolPanel title={asString(book.title) ?? i18n.t("assistant.tools.novelWork")}>
      <ToolTextBlock
        label={i18n.t("assistant.tools.rank")}
        value={displayValue(rank)}
      />
      <ToolTextBlock
        label={i18n.t("assistant.tools.author")}
        value={asString(book.author)}
      />
      <ToolTextBlock
        label={i18n.t("assistant.tools.category")}
        value={displayValue(book.categories)}
      />
      <ToolTextBlock
        label={i18n.t("assistant.tools.status")}
        value={asString(book.status)}
      />
      <ToolTextBlock
        label={i18n.t("assistant.tools.wordCount")}
        value={displayValue(book.word_count)}
      />
      <ToolTextBlock
        label={i18n.t("assistant.tools.chapterCountLabel")}
        value={displayValue(book.chapter_count)}
      />
      <Metrics metrics={metrics} />
      {Object.keys(sourceExtra).length > 0 ? (
        <ToolGroup label={i18n.t("assistant.tools.sourceExtra")}>
          <Box className="agent-tool-content-value agent-tool-content-plain-text">
            {displayValue(sourceExtra)}
          </Box>
        </ToolGroup>
      ) : null}
      <ToolTextBlock
        label={i18n.t("assistant.tools.introduction")}
        value={asString(book.introduction)}
      />
    </ToolPanel>
  );
}

export function NovelResearchToolMessage({ message }: NovelResearchToolMessageProps) {
  const data = getToolResultRecord(message);
  if (!data) {
    return (
      <ToolBody>
        <ToolNotice title={i18n.t("assistant.tools.noNovelResearchData")}>
          {i18n.t("assistant.tools.noNovelResearchDataDescription")}
        </ToolNotice>
      </ToolBody>
    );
  }

  if (message.toolName === "discover_novel_rankings") {
    const rankings = Array.isArray(data.rankings) ? data.rankings.filter(isRecord) : [];
    return (
      <ToolBody>
        <ToolTextBlock
          label={i18n.t("assistant.tools.site")}
          value={asString(data.site)}
        />
        <ToolTextBlock
          label={i18n.t("assistant.tools.query")}
          value={asString(data.query)}
        />
        <ToolTextBlock
          label={i18n.t("assistant.tools.fetchedAt")}
          value={asString(data.fetched_at)}
        />
        <ToolListBlock
          label={i18n.t("assistant.tools.rankingCount", { count: rankings.length })}
          values={rankings.map(
            (item) =>
              asString(item.name) ?? asString(item.rank_id) ?? i18n.t("assistant.tools.unknown"),
          )}
        />
      </ToolBody>
    );
  }

  if (message.toolName === "list_ranked_novels") {
    const ranking = isRecord(data.ranking) ? data.ranking : {};
    const items = Array.isArray(data.items) ? data.items.filter(isRecord) : [];
    return (
      <ToolBody>
        <ToolTextBlock
          label={i18n.t("assistant.tools.ranking")}
          value={asString(ranking.name)}
        />
        {items.map((item, index) => {
          const book = isRecord(item.book) ? item.book : {};
          return (
            <BookCard
              key={`${asString(book.source_book_id) ?? "book"}-${index}`}
              book={book}
              rank={item.rank}
              rankMetric={item.metric}
            />
          );
        })}
      </ToolBody>
    );
  }

  const book = isRecord(data.book) ? data.book : data;
  return (
    <ToolBody>
      <BookCard book={book} />
      {Array.isArray(book.chapters) && book.chapters.length > 0 ? (
        <ToolGroup label={i18n.t("assistant.tools.openingChapters")}>
          {book.chapters.filter(isRecord).map((chapter, index) => (
            <Box key={`${asString(chapter.source_chapter_id) ?? "chapter"}-${index}`}>
              <Text weight="medium">
                {asString(chapter.title) ?? `${i18n.t("assistant.tools.chapter")} ${index + 1}`}
              </Text>
              <Box className="agent-tool-content-plain-text novel-research-chapter-content">
                {asString(chapter.content)}
              </Box>
            </Box>
          ))}
        </ToolGroup>
      ) : null}
    </ToolBody>
  );
}
