echo "Installing dependencies..."
./install_dependencies.sh

echo "Backfilling data..."
./backfill.sh

echo "Building features..."
./build_features.sh

echo "Training model..."
./train_model.sh

echo "Done!"
