from dataclasses import dataclass

@dataclass
class Parameters:    
    mapping = {
        '[108204231] Mini Server P1': 'Configuration Server',
        '[120204241] Mini Server M3': 'Configuration Server',
        '[112206231] POS Screen': 'Configuration Monitor',
        '[122206241] POS Screen': 'Configuration Monitor',
        '[107206232] Handheld Smartphone L2s Pro': 'Configuration Handheld',
        '[101208231] Access Point EA U6 Pro': 'Configuration Access-Point',
        '[123210241] Printer DPT201': 'Configuration Printer',
        '[POS_H_Printer] POS Printer': 'Configuration Printer',
        '[113208231] Netgear Switch': 'Picking Switch',
        '[103203231] Cash Drawer': 'Picking Cash Drawer',
        '[111207241] POS Router': 'Configuration Router',
        '[132214251] POS Buzzer RBC': 'Picking Buzzer',
        '[102203241] POS Buzzer': 'Picking Buzzer',
        '[119209241] Payment Terminal': 'Picking Payment Terminal',
        '[121206231] Order Hardware': 'Picking and Configuration Order Terminal',
        '[121206231] Order Hardware (Monthly)': 'Picking and Configuration Order Terminal'
    }