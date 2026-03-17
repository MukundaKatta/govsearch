"""Tests for CLI commands."""

from click.testing import CliRunner

from govsearch.cli import cli


class TestCLI:
    def setup_method(self):
        self.runner = CliRunner()

    def test_version(self):
        result = self.runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_search(self):
        result = self.runner.invoke(cli, ["search", "environmental regulation"])
        assert result.exit_code == 0
        assert "Search Results" in result.output

    def test_search_with_type_filter(self):
        result = self.runner.invoke(
            cli, ["search", "cybersecurity", "--type", "legislation"]
        )
        assert result.exit_code == 0

    def test_search_no_results(self):
        result = self.runner.invoke(cli, ["search", "xyznonexistent12345"])
        assert result.exit_code == 0
        assert "No results" in result.output

    def test_search_invalid_type(self):
        result = self.runner.invoke(
            cli, ["search", "test", "--type", "invalidtype"]
        )
        assert result.exit_code == 0
        assert "Error" in result.output

    def test_analyze(self):
        result = self.runner.invoke(cli, ["analyze", "LEG-001"])
        assert result.exit_code == 0
        assert "Clean Air" in result.output

    def test_analyze_not_found(self):
        result = self.runner.invoke(cli, ["analyze", "NOPE-999"])
        assert result.exit_code == 0
        assert "not found" in result.output

    def test_citations(self):
        result = self.runner.invoke(cli, ["citations", "LEG-001"])
        assert result.exit_code == 0

    def test_citations_not_found(self):
        result = self.runner.invoke(cli, ["citations", "NOPE-999"])
        assert result.exit_code == 0
        assert "not found" in result.output

    def test_timeline(self):
        result = self.runner.invoke(cli, ["timeline", "cybersecurity"])
        assert result.exit_code == 0

    def test_report_markdown(self):
        result = self.runner.invoke(
            cli, ["report", "LEG-001", "--format", "markdown"]
        )
        assert result.exit_code == 0

    def test_report_text(self):
        result = self.runner.invoke(
            cli, ["report", "LEG-001", "--format", "text"]
        )
        assert result.exit_code == 0
        assert "SUMMARY" in result.output

    def test_stats(self):
        result = self.runner.invoke(cli, ["stats"])
        assert result.exit_code == 0
        assert "Total documents" in result.output
