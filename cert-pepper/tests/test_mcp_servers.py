"""Tests for MCP server modules — verifies FastMCP structure and serve() entry points."""

from __future__ import annotations

import inspect


class TestStudyEngineMCP:
    def test_mcp_is_fastmcp_instance(self):
        from mcp.server.fastmcp import FastMCP

        from cert_pepper.mcp.study_engine import mcp

        assert isinstance(mcp, FastMCP)

    def test_has_serve_function(self):
        from cert_pepper.mcp.study_engine import serve

        assert callable(serve)
        assert not inspect.iscoroutinefunction(serve)

    def test_tools_registered(self):
        from cert_pepper.mcp.study_engine import mcp

        tool_names = {t.name for t in mcp._tool_manager.list_tools()}
        assert "start_session" in tool_names
        assert "get_next_question" in tool_names
        assert "submit_answer" in tool_names
        assert "get_due_cards" in tool_names
        assert "end_session" in tool_names


class TestContentMCP:
    def test_mcp_is_fastmcp_instance(self):
        from mcp.server.fastmcp import FastMCP

        from cert_pepper.mcp.content import mcp

        assert isinstance(mcp, FastMCP)

    def test_has_serve_function(self):
        from cert_pepper.mcp.content import serve

        assert callable(serve)
        assert not inspect.iscoroutinefunction(serve)

    def test_tools_registered(self):
        from cert_pepper.mcp.content import mcp

        tool_names = {t.name for t in mcp._tool_manager.list_tools()}
        assert "get_explanation" in tool_names
        assert "get_question" in tool_names
        assert "search_questions" in tool_names
        assert "get_flashcard" in tool_names
        assert "lookup_acronym" in tool_names

    def test_get_explanation_accepts_context(self):
        """get_explanation tool must accept ctx: Context for MCP sampling."""
        from mcp.server.fastmcp import Context

        from cert_pepper.mcp.content import mcp

        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        assert "get_explanation" in tools


class TestAnalyticsMCP:
    def test_mcp_is_fastmcp_instance(self):
        from mcp.server.fastmcp import FastMCP

        from cert_pepper.mcp.analytics import mcp

        assert isinstance(mcp, FastMCP)

    def test_has_serve_function(self):
        from cert_pepper.mcp.analytics import serve

        assert callable(serve)
        assert not inspect.iscoroutinefunction(serve)

    def test_tools_registered(self):
        from cert_pepper.mcp.analytics import mcp

        tool_names = {t.name for t in mcp._tool_manager.list_tools()}
        assert "predict_score" in tool_names
        assert "get_weak_areas" in tool_names
        assert "get_study_recommendations" in tool_names
        assert "get_performance_trend" in tool_names
