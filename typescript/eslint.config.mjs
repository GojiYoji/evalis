import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import { defineConfig, globalIgnores } from 'eslint/config';

const ESLINT_IGNORE = ['src/__gen__', 'dist', 'node_modules'];

export default defineConfig(
  eslint.configs.recommended,
  tseslint.configs.recommended,
  globalIgnores(ESLINT_IGNORE, 'Ignore files')
);
