# AutoClaim Mudae

This project is a Python-based bot for automating actions on Discord bot Mudae using scheduled tasks. The bot interacts with Discord APIs to perform various tasks based on configurations set in a `config.json` file.

**Important:** This script will not work if your server is in a language other than English.

**Note:** This project is not yet complete!

## Overview

- **Bot.py**: Main script to schedule and execute bot actions.
- **Vars.py**: Provides configuration settings by reading from `config.json`.
- **Function.py**: Contains functions for bot actions such as rolling and claiming cards.
- **config.json**: Configuration file containing server-specific settings.

## Project Structure

```
.
├── Bot.py
├── Vars.py
├── Function.py
├── config.json
└── requirement.txt
```

### Bot.py

`Bot.py` schedules tasks for different configurations and runs them either immediately for testing or according to the schedule specified in `config.json`.

#### Key Features

- **Scheduling**: Jobs are scheduled to run at specific intervals.
- **Immediate Execution**: Run jobs immediately using the `--run-now` argument.
- **Logging**: Logs information about job execution and errors.

### Vars.py

`Vars.py` provides a function to load configurations from the `config.json` file.

#### Key Function

- `get_config(name)`: Reads and returns the configuration for a given `name`.

### Function.py

`Function.py` contains the core logic for interacting with Discord and handling card rolls and claims.

#### Key Functions

- `check_path_exists(jsonCard)`: Checks if the path exists in the provided JSON data.
- `simpleRoll(config)`: Handles the rolling and claiming process, including reacting to cards and handling reset claims.

### config.json

**Important:**

For the project to function correctly, you must rename the configuration file from `exampleConfig.json` to `config.json`.

This file includes server-specific configurations such as:

- Server and channel names/IDs
- User IDs
- Authentication tokens
- Roll commands and criteria for claiming cards
- Messages and texts to check for claim and reset

### How to Get Your Discord Token

**Warning:** Your token is sensitive. Use it responsibly and keep it private.

1. **Open Discord in Your Browser**:

   - Go to [discord.com](https://discord.com) and log in.

2. **Open Developer Tools**:

   - Press `F12` or `Ctrl + Shift + I` (Windows/Linux) or `Cmd + Option + I` (Mac).

3. **Go to Application Tab**:

   - Click on the "Application" tab in Developer Tools.

4. **Find Local Storage**:

   - On the left, under "Storage", select "Local Storage".
   - Click `https://discord.com`.

5. **Locate and Copy Token**:
   - Look for the entry labeled `token`.
   - Copy the value of this entry.

### How to Get Discord Server ID and Channel ID

**Note:** Ensure you have the appropriate permissions and handle these IDs privately.

#### Getting the Server ID

1. **Open Discord**:

   - Go to [discord.com](https://discord.com) and log in.

2. **Enable Developer Mode**:

   - Go to `User Settings` by clicking the gear icon next to your username.
   - Navigate to `Advanced` in the sidebar.
   - Toggle on `Developer Mode`.

3. **Find the Server ID**:
   - Right-click on the server name in the server list on the left side.
   - Select `Copy Server ID`.

#### Getting the Channel ID

1. **Open Discord**:

   - Ensure you are still logged in to Discord in your browser.

2. **Find the Channel ID**:
   - Right-click on the channel name (text or voice) within the server.
   - Select `Copy Channel ID`.

#### Getting the User ID

1. **Open Discord**:

   - Ensure you are still logged in to Discord in your browser.

2. **Right-Click on the User**:

   - Right-click on the user's name (or click on their profile picture) to open the context menu.

3. **Copy User ID**:
   - Click on **Copy ID** from the context menu.

**Note:** These IDs are unique and sensitive; handle them with care.

### Editable JSON Configuration

**1. `repeatMinute`**:

- **Description**: Specifies how often (in minutes) an action should repeat.
  You can change this value to adjust the interval. For example, setting it to `"30"` will make the action repeat every hour at minutes "30".

**2. `desiredSeries`**:

- **Description**: A list of series names that you are interested in.
  You can modify this array to include any series you want. For instance, adding `"One Piece"` will make the bot look for that series as well.

**3. `desiredKakeras`**:

- **Description**: A list of specific "kakera" types that you want to track.
  You can change the list to include or exclude different "kakera" types as needed. For example, if you want to stop tracking `"kakeraO"`, you can remove it from the list.

**4. `rollCommand`**:

- **Description**: The command that triggers the roll action.
  You can change this to any command you prefer. For example, changing it to `"ha"` will use that command instead. Refer to [WAIFU ROULETTE](https://mudae.fandom.com/wiki/List_of_Commands#WAIFU_ROULETTE) for available commands.

**5. `claimCriteria`**:

- **Description**: Defines the conditions under which a claim should be made.
  You can adjust the criteria. For instance, increasing the `"minKakeraPoints"` value to `600` will require more points to make a claim.

**6. `pokeRoll`**:

- **Description**: A boolean value that indicates whether to enable or disable the poke roll feature.
  You can set this to `true` or `false` depending on whether you want to enable or disable the feature.

## Setup

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Dependencies**

   Ensure you have the necessary libraries installed:

   ```bash
   pip install -r requirement.txt
   ```

3. **Configure `config.json`**

   Update `config.json` with your own Discord bot tokens, server IDs, channel IDs, and other configuration details.

4. **Run the Bot**

   To start the bot and schedule tasks:

   ```bash
   python Bot.py
   ```

## Usage

- **Scheduling Jobs**: Jobs are scheduled to run based on the configuration in `config.json`. The bot will handle rolling and claiming as per the defined criteria.
