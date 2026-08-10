{ pkgs ? import <nixpkgs> { config.allowUnfree = true; } }:

pkgs.mkShell {
  name = "kokoro-env";

  buildInputs = with pkgs; [
    python311
    python311Packages.pip
    python311Packages.virtualenv
    # Essential for audio processing and GPU support
    libsndfile
    cudaPackages.cudatoolkit
    cudaPackages.cudnn
    stdenv.cc.cc.lib
  ];

  shellHook = ''
    # Set up a virtual environment if it doesn't exist
    if [ ! -d ".venv" ]; then
      virtualenv .venv
    fi
    source .venv/bin/activate

    # Ensure library paths are set for CUDA and soundfile
    export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.cudaPackages.cudatoolkit}/lib:${pkgs.cudaPackages.cudnn}/lib:${pkgs.libsndfile}/lib:$LD_LIBRARY_PATH"
    
    echo "--- Kokoro TTS Environment Loaded ---"
    echo "Run 'pip install kokoro soundfile' if not already installed."
  '';
}
