# Machine-Monitoring
An Open Source Software to monitor three machines in Pop-up Factory: 
1. Laser Cutter: [OLSK-Small-Laser](https://github.com/Open-Lab-Starter-Kit/OLSK-Small-Laser)
3. CNC Router: [OLSK-Small-CNC](https://github.com/Open-Lab-Starter-Kit/OLSK-Small-CNC)
4. 3D Printer: [OLSK-Small-3D-Printer](https://github.com/Open-Lab-Starter-Kit/OLSK-Small-3D-Printer)

Machine Monitoring provides: 
1. States of machines: eg. Idle, Pause, Run or Job Done,
2. Power consumation of machine in Watt,
3. File name of the laoded gcode,
4. Start Time: when the job is started,
5. End Time: when the job is done,
6. The sumarize table of the jobs done by the machine.

The three machines data are saved into two csv files:
1. The state of the machines and the time when is occured.
2. The details of the Job ID, path of the gcode, start time and end time.

![Screen Shot 2023-03-13 at 12 52 50](https://user-images.githubusercontent.com/27281789/224694394-71e27d97-3190-4532-841b-41424c293412.png)

# How to run the machine monitoring?

## Requirement
1. MQTT Broker server
2. To run BCNC: machine must run GBRL.
3. To run Printrun: machine must run Marlin.

## Install the Mosquitto Server
Prerequisites:
1. An Ubuntu 20.04 server.
2. A non-root user with sudo rights.

https://mosquitto.org/

## How to run Machine Monitoring?
1. Update the broker_address variable into your broker hostname or ip address.

- Machine Monitoring Program
<code>broker_address= "pi-mqtt-server" #Update broker address</code>

- BCNC
Folder path: <code>bCNC/sender.py</code>
<code>self.broker_address= 'pi-mqtt-server'#"broker.emqx.io" #Update broker address</code>

- Printrun
Folder path: <code>printrun/printcore.py and printrun/pronterface.py</code>
<code>self.broker_address = "pi-mqtt-server"</code>

2. Run The programs.

  <code>cd bCNC-cnc</code>
  <code>python bCNC.py</code>
  
  <code>cd Printrun-master</code>
  <code>python pronterface.py</code>
  
  Author
--

The machine-monitoring software has been developed at **[InMachines Ingrassia GmbH](https://www.inmachines.net/)**.

<img src="https://irp.cdn-website.com/2b5ccdcd/dms3rep/multi/InMachines_Logo_positive_white.png" width="50%">

<br>

Development and programming by:
- **[Marcello Tania](https://marcellotania.com/)**

Contact
--

- daniele@inmachines.net
- [https://www.inmachines.net/](https://www.inmachines.net/)


License
--

The machine-monitoring is released under the following open source license:

- GNU Affero General Public License - **[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)**

The machine-monitoring documentation, pictures and presentation text of this repository are released under the following license:

- Creative-Commons-Attribution-ShareAlike 4.0 International - **[CC BY-SA 4.0](LICENSE_CC_BY_SA_4.0.txt)**


