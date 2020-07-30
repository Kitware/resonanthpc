<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>
    <!-- Base class for all PKs -->
    <AttDef Type="pk-base" BaseType="" Abstract="true" Version="0"></AttDef>

    <AttDef Type="pk-base-2" BaseType="pk-base" Abstract="true" Version="0"></AttDef>

    <!-- Base class for physical PKs -->
    <AttDef Type="pk-physical" BaseType="pk-base-2" Abstract="true" Version="0"></AttDef>

    <!-- Base class for BDF PKs -->
    <AttDef Type="pk-bdf" BaseType="pk-base-2" Abstract="true" Version="0"></AttDef>

    <!-- Inherit from pk-physical and copy bdf items-->
    <AttDef Type="pk-physical-bdf" BaseType="pk-physical" Abstract="true" Version="0"></AttDef>
  </Definitions>
</SMTK_AttributeResource>
