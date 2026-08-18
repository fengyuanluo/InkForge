import { Box, Button, Flex, Heading, Text, TextField } from "@radix-ui/themes";
import { LockKeyhole } from "lucide-react";
import { type FormEvent, useState } from "react";
import { useTranslation } from "react-i18next";

import { Spinner } from "@/components";
import { loginWithPassword } from "@/lib/api-client";

import "./password-login.css";

export function PasswordLogin() {
  const { t } = useTranslation();
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!password || isSubmitting) return;
    setIsSubmitting(true);
    setError(null);
    try {
      await loginWithPassword(password);
      window.location.reload();
    } catch {
      setError(t("auth.invalidPassword"));
      setIsSubmitting(false);
    }
  };

  return (
    <main className="password-login">
      <form
        className="password-login-form"
        onSubmit={handleSubmit}
      >
        <Flex
          direction="column"
          align="center"
          gap="4"
        >
          <LockKeyhole
            aria-hidden="true"
            size={32}
            strokeWidth={1.6}
          />
          <Heading
            as="h1"
            size="7"
          >
            InkForge
          </Heading>
          <Text
            as="label"
            htmlFor="inkforge-password"
            size="2"
            color="gray"
          >
            {t("auth.password")}
          </Text>
          <TextField.Root
            id="inkforge-password"
            className="password-login-input"
            type="password"
            value={password}
            autoFocus
            autoComplete="current-password"
            disabled={isSubmitting}
            style={{ width: "100%" }}
            onChange={(event) => setPassword(event.target.value)}
          />
          <Box className="password-login-error">
            {error ? (
              <Text
                size="2"
                color="red"
                role="alert"
              >
                {error}
              </Text>
            ) : null}
          </Box>
          <Button
            className="password-login-submit"
            type="submit"
            size="3"
            disabled={!password || isSubmitting}
            style={{ width: "100%" }}
          >
            {isSubmitting ? <Spinner size={18} /> : null}
            {t("auth.login")}
          </Button>
        </Flex>
      </form>
    </main>
  );
}
