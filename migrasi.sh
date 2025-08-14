#!/bin/bash


alembic revision --autogenerate -m "$1"
alembic upgrade head
