"""
Trigger configuration loading and initialization.
Backward-compatible module for loading trigger configurations from JSON.
"""
import json
import logging
from typing import List, Optional

from triggers import TriggerConfig, RegexTrigger, AlwaysTrigger
import config


def load_trigger_config(
    telegram_client,
    filename: str,
    debug: bool = False
) -> List[TriggerConfig]:
    """
    Load trigger configurations from JSON file.
    
    Args:
        telegram_client: Telethon TelegramClient instance
        filename: Path to trigger config JSON file
        debug: Enable debug logging
        
    Returns:
        List of TriggerConfig instances
        
    Raises:
        Exception: If config file cannot be loaded
    """
    logger = config.get_logger()
    
    try:
        with open(filename) as f:
            config_data = json.load(f)
            trigger_configs = []
            
            for user_config in config_data:
                # Create appropriate trigger type
                trigger_pattern = user_config.get('trigger')
                trigger = RegexTrigger(trigger_pattern) if trigger_pattern else AlwaysTrigger()
                
                # Create trigger configuration
                trigger_config = TriggerConfig(
                    name=user_config.get('name'),
                    trigger=trigger,
                    user_number=user_config.get('number'),
                    enable_message=user_config.get('message', False),
                    enable_call=user_config.get('call', False),
                    enable_visa_slots=user_config.get('check-visa-slots', False),
                )
                trigger_configs.append(trigger_config)
            
            log_output = "Loaded trigger configs:\n" + "\n".join(
                f"  - {cfg}" for cfg in trigger_configs
            )
            logger.info(log_output)
            
            if debug:
                print(log_output)
            
            return trigger_configs
            
    except Exception as e:
        error_msg = f"Failed to load trigger configs from '{filename}': {repr(e)}"
        logger.error(error_msg)
        raise


# Backward compatibility: expose old functions that used to be in this module
async def process_ocr_triggers(text, photo_path, message, trigger_config):
    """
    Deprecated: Use TriggerManager.process_ocr_triggers instead.
    Kept for backward compatibility.
    """
    logger = config.get_logger()
    logger.warning("process_ocr_triggers is deprecated. Use TriggerManager instead.")


async def process_check_visa_slot_triggers(text, trigger_config):
    """
    Deprecated: Use TriggerManager.process_visa_slots_triggers instead.
    Kept for backward compatibility.
    """
    logger = config.get_logger()
    logger.warning("process_check_visa_slot_triggers is deprecated. Use TriggerManager instead.")


if __name__ == '__main__':
    # Example usage for testing
    config.setup_logging()
    try:
        configs = load_trigger_config(None, "sample_trigger_configs.json", debug=True)
        print(f"\nSuccessfully loaded {len(configs)} trigger configurations")
    except Exception as e:
        print(f"Error: {e}")
