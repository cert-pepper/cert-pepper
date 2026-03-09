"""Tests for progress dashboard helper functions."""

from cert_pepper.cli.progress import domain_status_label


class TestDomainStatusLabel:
    """domain_status_label returns correct Rich markup based on accuracy and coverage."""

    def test_mastered_when_high_accuracy_and_sufficient_coverage(self) -> None:
        # 90% accuracy, 60 of 100 questions attempted (60% coverage)
        assert domain_status_label(0.90, 60, 100) == "[green]✓ Mastered[/green]"

    def test_on_track_replaces_mastered_when_coverage_below_threshold(self) -> None:
        # 90% accuracy but only 10 of 100 questions attempted (10% coverage)
        assert domain_status_label(0.90, 10, 100) == "[yellow]~ On Track[/yellow]"

    def test_on_track_at_exactly_50pct_coverage(self) -> None:
        # exactly 50% coverage is sufficient — Mastered allowed
        assert domain_status_label(0.90, 50, 100) == "[green]✓ Mastered[/green]"

    def test_on_track_mid_accuracy(self) -> None:
        # 75% accuracy regardless of coverage
        assert domain_status_label(0.75, 5, 100) == "[yellow]~ On Track[/yellow]"

    def test_on_track_mid_accuracy_sufficient_coverage(self) -> None:
        assert domain_status_label(0.75, 60, 100) == "[yellow]~ On Track[/yellow]"

    def test_weak_when_low_accuracy(self) -> None:
        # below 70% is Weak regardless of coverage
        assert domain_status_label(0.65, 60, 100) == "[red]✗ Weak[/red]"

    def test_weak_below_threshold_low_accuracy(self) -> None:
        # below 70% with low coverage is still Weak
        assert domain_status_label(0.50, 5, 100) == "[red]✗ Weak[/red]"

    def test_mastered_at_exactly_85pct_accuracy_and_50pct_coverage(self) -> None:
        assert domain_status_label(0.85, 50, 100) == "[green]✓ Mastered[/green]"

    def test_on_track_just_below_50pct_coverage_high_accuracy(self) -> None:
        # 49% coverage — not enough for Mastered
        assert domain_status_label(0.90, 49, 100) == "[yellow]~ On Track[/yellow]"
