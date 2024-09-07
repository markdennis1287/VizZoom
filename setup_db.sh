#!/bin/bash

echo "Setting up database..."
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
echo "Database setup complete."
