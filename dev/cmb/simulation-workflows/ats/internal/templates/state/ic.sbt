<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>

    <!-- TODO: initial conditions / "atomic constants" -->
    <!-- NOTE: this section is called initial conditions, but its not that. ATS wants to change the anme of this section to "atomic constants" -->
    <!-- NOTE: these "initial conditions" might also need to be used by the PKs... so we may want to put into a seperate XML file -->

    <!-- Base class for initial conditions -->
    <AttDef Type="ic-base" BaseType="" Abstract="true" Version="0">
    </AttDef>

    <!-- Class for Initialization of constant scalars -->
    <AttDef Type="ic-const-scalar" BaseType="ic-base" Version="0">
      <ItemDefinitions>
        <Double Name="value"></Double>
      </ItemDefinitions>
    </AttDef>

    <!-- Class for Initialization of constant vectors -->
    <AttDef Type="ic-const-vector" BaseType="ic-base" Version="0">
      <ItemDefinitions>
        <!-- NOTE: this can be 2 or 3D, i.e. the list can be 2 elements or 3. For now, we keep as 3-->
        <Double Name="value" NumberOfRequiredValues="3"></Double>
      </ItemDefinitions>
    </AttDef>

    <!-- The rest don't seem needed for the demos. -->

    <!-- TODO: Initialization of scalar fields -->
    <!-- <AttDef Type="ic-scalar-field" BaseType="ic-base" Version="0">
      <ItemDefinitions>
      </ItemDefinitions>
    </AttDef> -->

    <!-- TODO: Initialization of tensor fields -->
    <!-- <AttDef Type="ic-tensor-field" BaseType="ic-base" Version="0">
      <ItemDefinitions>
      </ItemDefinitions>
    </AttDef> -->

    <!-- TODO: Initialization from a file -->
    <!-- <AttDef Type="ic-file" BaseType="ic-base" Version="0">
      <ItemDefinitions>
      </ItemDefinitions>
    </AttDef> -->


    <!-- ////////////////////////////////////////////////////////////// -->
    <!-- TODO: Boundary conditions? or is it just the other two sections? -->

  </Definitions>
</SMTK_AttributeResource>
