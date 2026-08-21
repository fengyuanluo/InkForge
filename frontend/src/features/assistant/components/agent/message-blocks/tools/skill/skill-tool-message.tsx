import { Box } from "@radix-ui/themes";

import i18n from "@/i18n";
import type { AgentMessage } from "@/lib/agent.types";

import {
  ToolBody,
  ToolGroup,
  ToolListBlock,
  ToolNotice,
  ToolTextBlock,
} from "../shared/tool-message-shared";
import { getToolResultText } from "../shared/tool-message-utils";

interface SkillToolMessageProps {
  message: AgentMessage;
}

function decodeXmlText(value: string): string {
  const entities: Record<string, string> = {
    "&amp;": "&",
    "&lt;": "<",
    "&gt;": ">",
    "&quot;": '"',
    "&#x27;": "'",
  };
  return value.replace(/&(amp|lt|gt|quot|#x27);/g, (entity) => entities[entity] ?? entity);
}

function getAttribute(attributes: string, name: string): string | undefined {
  const match = attributes.match(new RegExp(`${name}="([^"]*)"`));
  return match?.[1] ? decodeXmlText(match[1]) : undefined;
}

function parseSkillOutput(text: string | undefined) {
  if (!text) return null;
  const opening = text.match(/<skill_content\b([^>]*)>/s);
  const reference = text.match(/<reference_content\b([^>]*)>/s);
  const attributes = opening?.[1] ?? reference?.[1] ?? "";
  const summaryText = text.match(/<skill_summary>([\s\S]*?)<\/skill_summary>/)?.[1];
  const metadataText = text.match(/<skill_metadata>([\s\S]*?)<\/skill_metadata>/)?.[1];
  let metadata: Record<string, unknown> = {};
  if (metadataText) {
    try {
      const parsed: unknown = JSON.parse(decodeXmlText(metadataText));
      if (parsed && typeof parsed === "object" && !Array.isArray(parsed)) {
        metadata = parsed as Record<string, unknown>;
      }
    } catch {
      // Keep the body visible when metadata is from an older or malformed result.
    }
  }
  const references = Array.from(text.matchAll(/<ref>([^<]+)<\/ref>/g)).map((match) =>
    decodeXmlText(match[1]),
  );
  const body = text
    .replace(
      /<skill_content\b[^>]*>|<\/skill_content>|<reference_content\b[^>]*>|<\/reference_content>/g,
      "",
    )
    .replace(/<skill_summary>[\s\S]*?<\/skill_summary>/, "")
    .replace(/<skill_metadata>[\s\S]*?<\/skill_metadata>/, "")
    .replace(/<skill_references>[\s\S]*?<\/skill_references>/, "")
    .trim();
  return {
    name: getAttribute(attributes, "name") ?? getAttribute(attributes, "skill_name"),
    summary: summaryText ? decodeXmlText(summaryText) : getAttribute(attributes, "summary"),
    referenceName: getAttribute(attributes, "reference_name"),
    metadata,
    references,
    body,
  };
}

function formatMetadata(value: unknown): string | undefined {
  if (typeof value === "string") return value;
  if (value === null || value === undefined) return undefined;
  try {
    return JSON.stringify(value, null, 2);
  } catch {
    return String(value);
  }
}

export function SkillToolMessage({ message }: SkillToolMessageProps) {
  const parsed = parseSkillOutput(getToolResultText(message));
  if (!parsed) {
    return (
      <ToolBody>
        <ToolNotice title={i18n.t("assistant.tools.skillNoStructuredContent")}>
          {getToolResultText(message) ?? i18n.t("assistant.tools.skillNoStructuredContent")}
        </ToolNotice>
      </ToolBody>
    );
  }

  const metadataEntries = Object.entries(parsed.metadata);
  return (
    <ToolBody>
      <ToolTextBlock
        label={i18n.t("assistant.tools.skillName")}
        value={parsed.name}
      />
      <ToolTextBlock
        label={i18n.t("assistant.tools.skillSummary")}
        value={parsed.summary}
      />
      <ToolTextBlock
        label={i18n.t("assistant.tools.referenceName")}
        value={parsed.referenceName}
      />
      {metadataEntries.length > 0 ? (
        <ToolGroup label={i18n.t("assistant.tools.skillMetadata")}>
          <Box className="agent-tool-content-value agent-tool-content-plain-text">
            {metadataEntries.map(([key, value]) => (
              <Box key={key}>
                <strong>{key}</strong>: {formatMetadata(value)}
              </Box>
            ))}
          </Box>
        </ToolGroup>
      ) : null}
      <ToolListBlock
        label={i18n.t("assistant.tools.skillReferences")}
        values={parsed.references}
      />
      <ToolTextBlock
        label={i18n.t("assistant.tools.content")}
        value={parsed.body}
      />
    </ToolBody>
  );
}
