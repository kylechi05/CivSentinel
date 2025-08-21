import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";
import eslintPluginImport from "eslint-plugin-import";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
    baseDirectory: __dirname,
});

const eslintConfig = [
    ...compat.extends(
        "next/core-web-vitals",
        "next/typescript",
        "eslint-config-prettier",
    ),
    {
        plugins: {
            import: eslintPluginImport,
        },
        rules: {
            indent: ["warn", 4],
            "import/no-unresolved": "error",
        },
    },
];

export default eslintConfig;
