#!/bin/bash
black laserchess tests
py.test --cov laserchess
