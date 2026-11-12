# Deviations and engineering repairs

The target was changed during feasibility selection, before protocol freeze or final evaluation. See decisions.md.

1. Windows unit tests passed 40 cases. A test-only closed-form AP oracle emitted log(0) at p=1; it was changed to handle that endpoint explicitly. Production metric code and protocol unchanged.
2. The first Windows final command failed before metric calculation: a source-hash dictionary used Windows path separators but lookup used POSIX separators. Changed path serialization to as_posix(), committed the repair, retained failed_run_path_separator.log, and reran. No outcome-driven scientific changes.
3. The initial Linux test invocation from the parent directory could not import src. Rerunning from the documented project root passed all 40 tests. This command-context error did not affect the Windows study.
4. Optional official LaTeX build was unavailable because its packages/bibliography backend were missing. Used the permitted alternative PDF build and mandatory metadata structure. See manuscript/TEMPLATE_ADAPTATION.md.
5. No post-freeze scientific protocol changes. Source hashes distinguish the pre-portability Linux run from the corrected Windows implementation; their primary values agree within 1e-12.

6. Publication preparation: incremental process-output checks timed out. Cached tail retrieval confirmed successful private repository creation; no duplicate creation was attempted.
7. An initial staging command stopped before execution because its publication directory was absent; the directory was created. ZIP timestamp handling was then made portable with strict_timestamps=False after metadata-only transfer. Research file contents and actual ISO experiment timestamps were unchanged. The private staging upload subsequently completed.
