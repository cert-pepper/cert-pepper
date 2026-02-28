"""Tests for cert_pepper/ingestion/exam_yaml.py."""

from __future__ import annotations

import pytest
from pathlib import Path

from cert_pepper.ingestion.exam_yaml import parse_exam_yaml
from cert_pepper.models.content import ExamConfig


class TestParseExamYaml:
    def test_parses_valid_yaml(self, tmp_path):
        yaml_text = """\
code: "TEST-101"
name: "Test Exam"
vendor: "TestVendor"
passing_score: 700
max_score: 900
domains:
  - number: 1
    name: "Domain One"
    weight_pct: 40.0
  - number: 2
    name: "Domain Two"
    weight_pct: 60.0
"""
        path = tmp_path / "exam.yaml"
        path.write_text(yaml_text)
        config = parse_exam_yaml(path)

        assert config.code == "TEST-101"
        assert config.name == "Test Exam"
        assert config.vendor == "TestVendor"
        assert config.passing_score == 700
        assert config.max_score == 900
        assert len(config.domains) == 2
        assert config.domains[0].number == 1
        assert config.domains[0].name == "Domain One"
        assert config.domains[0].weight_pct == 40.0

    def test_parses_real_security_plus_yaml(self):
        """Parse the actual exam.yaml in examples/security-plus/."""
        from pathlib import Path
        repo_root = Path(__file__).parent.parent
        exam_yaml = repo_root / "examples" / "security-plus" / "exam.yaml"
        if not exam_yaml.exists():
            pytest.skip("examples/security-plus/exam.yaml not present")

        config = parse_exam_yaml(exam_yaml)
        assert config.code == "SY0-701"
        assert len(config.domains) == 5

    def test_domain_weights_sum_to_100(self, tmp_path):
        yaml_text = """\
code: "X"
name: "X"
vendor: "X"
domains:
  - number: 1
    name: "A"
    weight_pct: 30.0
  - number: 2
    name: "B"
    weight_pct: 70.0
"""
        path = tmp_path / "exam.yaml"
        path.write_text(yaml_text)
        config = parse_exam_yaml(path)
        total = sum(d.weight_pct for d in config.domains)
        assert abs(total - 100.0) < 0.01

    def test_domain_weights_not_summing_to_100_raises(self, tmp_path):
        yaml_text = """\
code: "BAD"
name: "Bad Exam"
vendor: "V"
domains:
  - number: 1
    name: "A"
    weight_pct: 30.0
  - number: 2
    name: "B"
    weight_pct: 50.0
"""
        path = tmp_path / "exam.yaml"
        path.write_text(yaml_text)
        with pytest.raises(ValueError, match="sum"):
            parse_exam_yaml(path)

    def test_missing_file_raises_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            parse_exam_yaml(tmp_path / "nonexistent.yaml")

    def test_missing_required_field_raises_validation_error(self, tmp_path):
        yaml_text = """\
name: "Missing code"
vendor: "V"
domains: []
"""
        path = tmp_path / "exam.yaml"
        path.write_text(yaml_text)
        with pytest.raises(Exception):  # Pydantic ValidationError
            parse_exam_yaml(path)

    def test_vendor_defaults_to_empty_string(self, tmp_path):
        yaml_text = """\
code: "X"
name: "Exam"
domains:
  - number: 1
    name: "D"
    weight_pct: 100.0
"""
        path = tmp_path / "exam.yaml"
        path.write_text(yaml_text)
        config = parse_exam_yaml(path)
        assert config.vendor == ""
