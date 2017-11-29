Instrucciones de instalación de la Cloudera Quickstart VM
=========================================================

Siga las siguientes instrucciones para la descarga e instalación de la Máquina Virtual (MV) Cloudera Quickstart para VirtualBox.
Las capturas de pantalla son de un ordenador Mac, pero las instrucciones deberían ser también válidas para Windows. En caso de encontrar algún problema revise los foros de soporte. 

1. Instale VirtualBox. Vaya a https://www.virtualbox.org/wiki/Downloads  para descargar e instalar VirtualBox en su ordenador.

2. Vaya a la página de descargas de Cloudera (https://www.cloudera.com/downloads/quickstart_vms.html)  y descargue el fichero que contiene la máquina virtual, siguiendo los pasos a continuación: 
    
    * Seleccione la plataforma *VirtualBox*
    
        ![select_platform](_static/select_platform.png) 
    
    * Haga clic en el botón *GET IT NOW*
    
        ![get_it_now](_static/get_it_now.png)
    
    * Rellene el formulario y haga clic en *Continue*
    
        ![fill_in_continue](_static/fill_in_continue.png)
        
    * Acepte los Términos y Condiciones y haga clic en *SUBMIT* para iniciar la descarga. 
    
        ![accept_TC_continue](_static/accept_TC_continue.png)
        
    El tamaño de la MV es superior a 4GiB, así que este proceso puede tardar un poco.

3. Extraiga la MV de Cloudera:

    Haga clic con el botón derecho del ratón en *cloudera-quickstart-vm-X.X.X-0-virtualbox.zip* y seleccione "Extraer Todo ..."

4. Arranque la aplicación VirtualBox.

5. Import la MV en la aplicación yendo a *Archivo -> Importar servicio virtualizado*

    ![import appliance](_static/1YHbnrvaEeWbLwqB7NyVNQ_18b3b1a489e3d9ce53e7b3975d38910a_Untitled.png)

6. Clique en el icono de la Carpeta

    ![folder icon](_static/EUf7pLvbEeWHhw4MvaB3nw_98aed876336d826ba38b3ff967f59341_Untitled1.png)

7. Seleccione el fichero *cloudera-quickstart-vm-X.X.X-0-virtualbox.ovf* de la carpeta donde descomprimió la MV VirtualBox y clique en *Abrir*

    ![ovf select](_static/kvXZY7vdEeW6FApX76Rguw_04212a7fd040cdd18258055596ba98a7_Untitled2.png)

8. Clique *Siguiente* para continuar.

    ![ovf_next](_static/05MjOLvdEeWHhw4MvaB3nw_d8ba793c18835387ddb02defba586569_Untitled3.png)

9. Clique Importar.

    ![ovf_import](_static/8ZNYCrvdEeWg-hLO0rEOAw_af0950df42ffc15de1631a512eb6aa46_Untitled4.png)

10. La MV se importará en la aplicación. Esta operación puede tardar varios minutos.

    ![vm_import](_static/AoLTKrveEeWW3xLV17cwNw_b371ba33d261f8b00ac357da5590e2d6_Untitled5.png)

11. Cuando la importación haya finalizado, la MV *cloudera-quickstart-vm...* aparecerá en la parte izquierda de la ventana de VirtualBox. Seleccionela y clique en el botón de "Iniciar" para arrancarla.

    ![vm_launch](_static/HdSw4rveEeWg-hLO0rEOAw_8e77353aeafcc336742baf76aa647c8a_Untitled6.png)

12. Arranque de la MV. El proceso de arranque de la Máquina Virtual puede tardar varios minutos, debido a que deben iniciarse multitud de herramientas de Hadoop.

    ![vm_boot](_static/VKeShLveEeWHhw4MvaB3nw_bfb04aa6c0c0e0705514e617f45b1a86_Untitled7.png)

13. Escritorio de la MV. Una vez completado el proceso de arranque, aparecerá el escritorio con un navegador abierto.

    ![vm_desktop](_static/vlPlZruyEeWHhw4MvaB3nw_f128a6a6651d531d31a01f8c4ed79f53_vm-started.png)

14. Apagar la MV de Cloudera. Para poder cambiar la configuración de la MV de Cloudera, es necesario apagarla. Si la MV está corriendo, clique en botón *System* de la barra de herramientas superior, y luego en *Shut Down...*.

	![vm_shutdown](_static/GsZrdF8SEeafuBI2oAYa8w_a598868bbbe0914586f3ee1f17313b71_shutdown.png)

15. A continuació clique en *Shut Down*:

    ![vm_shutdown_bis](_static/DdZY018SEeafuBI2oAYa8w_8e1003755bdeb2ce175c3850e9cd0124_shutdown2.png)


