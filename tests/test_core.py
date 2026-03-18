"""Tests for Govsearch."""
from src.core import Govsearch
def test_init(): assert Govsearch().get_stats()["ops"] == 0
def test_op(): c = Govsearch(); c.analyze(x=1); assert c.get_stats()["ops"] == 1
def test_multi(): c = Govsearch(); [c.analyze() for _ in range(5)]; assert c.get_stats()["ops"] == 5
def test_reset(): c = Govsearch(); c.analyze(); c.reset(); assert c.get_stats()["ops"] == 0
def test_service_name(): c = Govsearch(); r = c.analyze(); assert r["service"] == "govsearch"
